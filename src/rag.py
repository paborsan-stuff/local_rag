import os
from modules.QueryContainerFile import QueryContainer
import argparse
from modules.ConvenienceFunctions import Convenience


def parse_args():
    parser = argparse.ArgumentParser(description="codesign: cache_vector_db mode")

    parser.add_argument(
        "--use-cache", action="store_true", help="Use cached vector db"
    )

    return parser.parse_args()


def setup(setup_rag):

    rag_param = setup_rag.load_env()

    setup_rag.print_rag_param(rag_param)
    setup_rag.fetch_text_emb_model(rag_param["embedding_model"])
    setup_rag.fetch_llm_model()

    return rag_param


def answer_query(prompt: str) -> str:
    """
    Function for testing the connection.
    This version is hardcoded to return "Testing".
    """
    # This function is called from api_server.py to get the response that will be sent to the UI.
    return "Testing"


def main():

    project_root = os.path.dirname(os.path.abspath(__file__))  # …/src
    tmp_dir      = os.path.join(project_root, "tmp")
    setup_rag = Convenience(project_root)

    rag_param = setup(setup_rag)
    args = parse_args()
    docs, file_names = setup_rag.load_paragraphs_from_folder("TestData")

    if args.use_cache == True:
        print ("Using cached vector db")

    query_container = QueryContainer(docs, file_names, args, cache_dir=tmp_dir)
    query_container.compute_get_vector_store(rag_param)
    
    query_str = ("Muéstrame un reclinador lujoso")

    llm_response = query_container.retrieval_llm_response(query_str)
    print(llm_response)


if __name__ == "__main__":
    main()
