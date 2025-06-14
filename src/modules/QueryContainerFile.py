import os
import json
import numpy as np
from modules.EmbeddingGenerator import EmbeddingGenerator
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from modules.LLMAdapter import LLMAdapter
from modules.Chunker import Chunker
from modules.FileIntegrityChecker import FileIntegrityChecker

class QueryContainer:
    def __init__(self, docs, file_names, args, cache_dir):

        self.cache_dir = cache_dir

        hash_dir      = self.cache_dir + "/TestData"
        self.tmp_dir  = os.path.join(self.cache_dir, "tmp")

        self.emb_mdl = EmbeddingGenerator(self.tmp_dir)
        self.integrity = FileIntegrityChecker(hash_dir, hash_file="vdb/hashes.json", algorithm="md5")
        self.docs = docs
        self.file_names = file_names
        self.args = args
        self.doc_id_map  = None
        self.vector_store = None

    def compute_get_vector_store(self, rag_param):

        doc_id_map = {}

        if os.path.isfile("vdb/doc_id_map.json"):
            if os.path.isfile("vdb/vector_db.json"):
                if self.integrity.check_integrity():
                    with open("vdb/doc_id_map.json", "r", encoding="utf-8") as f:
                        doc_id_map = json.load(f)
                        print("doc_id_map loaded")
                    with open("vdb/vector_db.json", "r", encoding="utf-8") as f:
                        vector_store = json.load(f)
                        print("vector store loaded")
            
            else:
                print("Hash File does not exist")
                doc_id_map = self._doc_id_compute(rag_param, doc_id_map)
                vector_store = self.get_query_vector_store_db(doc_id_map, self.args.use_cache)

        if self.integrity.check_integrity() == False:
            print("No doc_id_map defined, creating...")
            doc_id_map = self._doc_id_compute(rag_param, doc_id_map)
            vector_store = self.get_query_vector_store_db(doc_id_map, self.args.use_cache)

        if not vector_store:
            raise ValueError("Empty Vector data base")
        
        self.doc_id_map = doc_id_map
        self.vector_store = vector_store

        return vector_store

    def _doc_id_compute(self, rag_param, doc_id_map):
        for doc, file_name in zip(self.docs, self.file_names):
            mdl_chunker = Chunker(rag_param["embedding_model"], input_text=doc)
            chunks = mdl_chunker.process_paragraphs()
            doc_id_map[file_name] = chunks
        
        with open('vdb/doc_id_map.json', 'w') as f:
            json.dump(doc_id_map, f, indent=2)

        self.integrity.save_hashes()
        
        return doc_id_map

    def retrieval_llm_response(self, query_str):
        # Prepare LLM prompt
        system_prompt = """
            You are an intelligent document analysis assistant.

            You will receive a user query and a block of context extracted from one or more documents.

            Your job is to answer the user's query based **only on the context provided** in a natural way.

            Always answer. Never remain silent.

        """

        local_dir = self.tmp_dir + "/llm"
        top_score, retrieved_docs = self.process_query_str(query_str)

        # 1. Descarga del modelo (sin usar symlinks)
        model_path = hf_hub_download(
            repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
            filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )

        llm = Llama(model_path=model_path, n_gpu_layers=10)
        instance_model = LLMAdapter(llm)

        llm_prompt = LLMAdapter.construct_prompt(
            system_prompt=system_prompt,
            retrieved_docs=retrieved_docs,
            user_query=query_str
        )

        response = instance_model.stream_and_buffer_response(base_prompt=llm_prompt, max_tokens=800)

        return response, top_score, retrieved_docs
    
    def rag_or_chat(self, query_str):
        # Prepare LLM prompt
        system_prompt = """
            You are an assistant that must choose only one of two possible actions based on the user's query.

            You will receive:

                A query from the user
                An optional context (text extracted from documents)

            Your rules:

                1.- If the query is general conversation reply naturally witouth inventing things.
                2.- If the query asks for something inside the documents (e.g., “according to the text”, “find”, “what does it say in the file”), then do not answer the question. Just reply exactly like this:
                RAG: [keywords]
                Use English keywords based on the query and context.

            You must always choose only one:

                If rule 1 respond naturally,
                If rule 2 respond only with RAG: [keywords] (if it’s document-related).
                Never mix both. Never ask the user to clarify.

            You must always reply.
        """

        local_dir = self.tmp_dir + "/llm"
        #top_score, retrieved_docs = self.process_query_str(query_str)

        # 1. Descarga del modelo (sin usar symlinks)
        model_path = hf_hub_download(
            repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
            filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )

        llm = Llama(model_path=model_path, n_gpu_layers=10)
        instance_model = LLMAdapter(llm)

        llm_prompt = LLMAdapter.construct_chatting_prompt(
            system_prompt=system_prompt,
            user_query=query_str
        )

        response = instance_model.stream_and_buffer_response(base_prompt=llm_prompt, max_tokens=800)

        return response#, top_score, retrieved_docs


    def process_query_str(self, query_str):
        query_str_embedding = np.array(self.emb_mdl.compute_embeddings(query_str))

        top_score, middle_score, last_score = self.find_db_vector_best_dot_score(query_str_embedding, top_k=3)
        print(top_score)
        retrieved_docs = self.doc_id_map[top_score[0]][top_score[1]]['text']
        return top_score, retrieved_docs


    def get_query_vector_store_db(self, doc_id_map, use_cache):

        vector_store = {}

        if use_cache == False:
            vector_store = self.compute_creation_vector_store(doc_id_map)
            os.makedirs(os.path.dirname("vdb/vector_db.json"), exist_ok=True)
            with open('vdb/vector_db.json', 'w') as f:
                json.dump(vector_store, f, indent=2)
        else: 
            with open('vdb/vector_db.json', 'r') as f:
                try:
                    dbjson = json.load(f)
                    if not dbjson:
                        vector_store = self.compute_creation_vector_store(doc_id_map)
                    else:
                        print("Vector db file cached!")
                        vector_store = dbjson
                except json.JSONDecodeError:
                    print(f"[ERROR] Invalid JSON format in vdb/vector_db.json ")
                    return None
        return vector_store

    def compute_creation_vector_store(self, doc_id_map):

        vector_store = {}

        for doc_id, chunks in doc_id_map.items():
            vector_store[doc_id] = self.emb_mdl.create_vector_store(chunks)

        return vector_store
    
    def find_db_vector_best_dot_score(self, query_str_embedding, top_k=3):
        """
        This function takes in a vector store dictionary, a query string, and an int 'top_k'.
        It computes embeddings for the query string and then calculates the cosine similarity against every chunk embedding in the dictionary.
        The top_k matches are returned based on the highest similarity scores.
        """
        # Get the embedding for the query string
        scores = {}
        # Calculate the cosine similarity between the query embedding and each chunk's embedding
        for doc_id, chunks in self.vector_store.items():
            for chunk_id, chunk_embedding in chunks.items():
                chunk_embedding_array = np.array(chunk_embedding)
                # Normalize embeddings to unit vectors for cosine similarity calculation

                norm_query = np.linalg.norm(query_str_embedding)
                norm_chunk = np.linalg.norm(chunk_embedding_array)
                if norm_query == 0 or norm_chunk == 0:
                    # Avoid division by zero
                    score = 0
                else:
                    score = np.dot(chunk_embedding_array, query_str_embedding) / (norm_query * norm_chunk)
                    #print (score)

                # Store the score along with a reference to both the document and the chunk
                scores[(doc_id, chunk_id)] = score

                # Sort scores and return the top_k results
                sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
                top_results = [(doc_id, chunk_id, score) for ((doc_id, chunk_id), score) in sorted_scores]

        return top_results    