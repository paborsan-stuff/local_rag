import numpy as np
from modules.chunker import Chunker
from modules.EmbeddingGenerator import EmbeddingGenerator
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from modules.LLMAdapter import LLMAdapter
import argparse
import json
from convience_functions import (
    load_env,
    fetch_text_emb_model,
    fetch_llm_model,
    find_db_vector_best_dot_score,
    print_rag_param,
    load_paragraphs_from_folder,
)


def parse_args():
    parser = argparse.ArgumentParser(description="codesign: cache_vector_db mode")

    parser.add_argument(
        "--use-cache", action="store_true", help="Use cached vector db"
    )

    return parser.parse_args()


def setup():
    rag_param = load_env()

    print_rag_param(rag_param)

    # Fetch models if not already downloaded

    fetch_text_emb_model(rag_param["embedding_model"])
    fetch_llm_model()
    return rag_param

def get_query_vector_store_db(emb_mdl, doc_id_map, use_cache):
    vector_store = {}

    if use_cache == False:
        vector_store = create_vector_store(emb_mdl, doc_id_map, vector_store)
        with open('vdb/vector_db.json', 'w') as f:
            json.dump(vector_store, f)
    else: 
        with open('vdb/vector_db.json', 'r') as f:
            try:
                dbjson = json.load(f)
                if not dbjson:
                    vector_store = create_vector_store(emb_mdl, doc_id_map, vector_store)
                else:
                    print("Vector db file cached!")
                    vector_store = dbjson
            except json.JSONDecodeError:
                print(f"[ERROR] Invalid JSON format in vdb/vector_db.json ")
                return None
    return vector_store

def create_vector_store(emb_mdl, doc_id_map, vector_store):

    vector_store = {}

    for doc_id, chunks in doc_id_map.items():
        print("chunks", chunks)
        vector_store[doc_id] = emb_mdl.create_vector_store(chunks)

    return vector_store

def main():

    rag_param = setup()
    emb_mdl = EmbeddingGenerator("tmp")
    args = parse_args ()
    docs, file_names = load_paragraphs_from_folder("TestData")

    if args.use_cache == True:
        print ("Using cached vector db")

    all_tokenized_chunks = {}
    doc_id_map = {}
    for doc, file_name in zip(docs, file_names):
        mdl_chunker = Chunker(rag_param["embedding_model"], input_text=doc)
        chunks = mdl_chunker.process_paragraphs()
        doc_id_map[file_name] = chunks

    vector_store = get_query_vector_store_db(emb_mdl, doc_id_map, args.use_cache)

    if not vector_store:
        raise ValueError("Empty Vector data base")
    
    query_str = (
        "I am looking to a place to watch movies with my family, what do you recommend?"
    )

    query_str_embedding = np.array(emb_mdl.compute_embeddings(query_str))

    for doc_id, chunks in doc_id_map.items():
        print("chunks", chunks)
        vector_store[doc_id] = emb_mdl.create_vector_store(chunks)
        matches = find_db_vector_best_dot_score(
            vector_store[doc_id], query_str_embedding
        )
        print(doc_id, matches)



#
#    query_str_embedding = np.array(emb_mdl.compute_embeddings(query_str))
#    print(query_str_embedding)
#
#    matches = find_db_vector_best_dot_score(vectorized_chunks, query_str_embedding)
#    print("Top matches:", matches)
#
#    # Gather retrieved docs from top matches
#    retrieved_docs = "\n".join(
#        [all_tokenized_chunks[doc_id] for (doc_id, chunk_id, score) in matches]
#    )

#    # Prepare LLM prompt
#    system_prompt = """
# You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
#
# Your job is to understand the request, and answer based on the retrieved context.
# """
#
#    llm = Llama(model_path="tmp/llm/mistral-7b-instruct-v0.2.Q3_K_L.gguf", n_gpu_layers=1)
#    instance_model = LLMAdapter(llm)
#
#    llm_prompt = LLMAdapter.construct_prompt(
#        system_prompt=system_prompt,
#        retrieved_docs=retrieved_docs,
#        user_query=query_str
#    )
#
#    response = instance_model.stream_and_buffer_response(base_prompt=llm_prompt, max_tokens=800)
#    print("LLM Response:", response)


if __name__ == "__main__":
    main()
