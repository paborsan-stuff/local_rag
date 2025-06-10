import numpy as np
from modules.chunker import Chunker
from modules.EmbeddingGenerator import EmbeddingGenerator
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from modules.LLMAdapter import LLMAdapter
from convience_functions import load_env, fetch_text_emb_model, fetch_llm_model, compute_matches, print_rag_param, load_paragraphs_from_folder
TEST_PARAGRAPHS = """Basement home theater seating in black leather, includes three reclining seats with cup holders and storage compartments.
Designed for ultimate comfort and convenience during movie nights. 

Manufactured by Luxe Seating. Dimensions per seat: 36"W x 40"D x 40"H.
"""
def setup():
    rag_param = load_env()
   
    print_rag_param (rag_param)

    # Fetch models if not already downloaded

    fetch_text_emb_model(rag_param["embedding_model"])
    fetch_llm_model()
    return rag_param

def main():
    rag_param = setup()

    # Load all paragraphs from all text files in TestData
    docs, file_names = load_paragraphs_from_folder("TestData")
    print("Number of paragraphs:", len(docs))

    all_tokenized_chunks = {}
    doc_id_map = {}
    for idx, doc in enumerate(docs):
        #print (doc)
        mdl_chunker = Chunker(rag_param["embedding_model"], input_text=doc)
        chunks = mdl_chunker.process_paragraphs()
        #for chunk_id, chunk_text in chunks.items():
        #    key = f"{file_names[idx]}_{idx}_{chunk_id}"
        #    all_tokenized_chunks[key] = chunk_text

        doc_id_map[idx] = chunks

    print (doc_id_map)

    #print("tokenized_chunks", all_tokenized_chunks)
    #print(doc_id_map)

    emb_mdl = EmbeddingGenerator("tmp")
    vector_store = {}
    for doc_id, chunks in doc_id_map.items():
        print("chunks", chunks)
        vector_store[doc_id] = emb_mdl.create_vector_store(chunks)

    print("vector_store", vector_store)

#
#    query_str = "I am looking to a place to watch movies with my family, what do you recommend?"
#    query_str_embedding = np.array(emb_mdl.compute_embeddings(query_str))
#    print(query_str_embedding)
#
#    matches = compute_matches(vectorized_chunks, query_str_embedding)
#    print("Top matches:", matches)
#
#    # Gather retrieved docs from top matches
#    retrieved_docs = "\n".join(
#        [all_tokenized_chunks[doc_id] for (doc_id, chunk_id, score) in matches]
#    )

#    # Prepare LLM prompt
#    system_prompt = """
#You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
#
#Your job is to understand the request, and answer based on the retrieved context.
#"""
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
