import numpy as np
import os
from modules.chunker import Chunker
from modules.EmbeddingGenerator import EmbeddingGenerator
import modules.QueryContainerFile
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
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

def main():

    rag_param = setup()
    emb_mdl = EmbeddingGenerator("tmp")
    args = parse_args ()
    docs, file_names = load_paragraphs_from_folder("TestData")

    if args.use_cache == True:
        print ("Using cached vector db")

    doc_id_map = {}
    vector_store = compute_get_vector_store(rag_param, emb_mdl, args, docs, file_names, doc_id_map)
    
    query_str = ("ceramic")

    modules.QueryContainerFile.retrieval_llm_response(query_str)


if __name__ == "__main__":
    main()
