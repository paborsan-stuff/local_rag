import yaml
from modules.Chunker import Chunker
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

def load_env():

    env_path = Path("env/config.yaml")
    with open(env_path, "r") as file:
        config = yaml.safe_load(file)
    # Use .get() with an empty dictionary as default for robustness
    return config


def main():

    rag_param = load_env()
    print("Chunk Size", rag_param["chunk_size"])
    print("Model name", rag_param["model_name"])
    print("Model types", rag_param["document_types"])

    mdl_chunker = Chunker(rag_param["model_name"])

    mdl_chunker.process_paragraphs()

    model_name = "BAAI/bge-small-en-v1.5"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    tokenizer.save_pretrained("model/tokenizer")
    model.save_pretrained("model/embedding")
    
    #
    #
    # Creates text chunk based on tokens for processing
    #
    # docs = chunker.document_chunker(directory_path='/home/paborsan/Documents/RAG_Data',
    #                        model_name='BAAI/bge-small-en-v1.5',
    #                        chunk_size=256)
    #
    # vec_store = indexer.create_vector_store(docs)
    #
    # matches = indexer.Indexer.compute_matches(vector_store=vec_store,
    #            query_str="Pablo",
    #            top_k=3)
    # print(matches)


if __name__ == "__main__":
    main()
