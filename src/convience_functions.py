import numpy as np
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
import yaml

def load_env():

    env_path = Path("env/config.yaml")
    with open(env_path, "r") as file:
        config = yaml.safe_load(file)
    # Use .get() with an empty dictionary as default for robustness
    return config


def fetch_text_emb_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    tokenizer.save_pretrained("tmp/tokenizer")
    model.save_pretrained("tmp/embedding")


def fetch_llm_model():

    # Target directory and model info
    target_dir = "tmp/llm"
    os.makedirs(target_dir, exist_ok=True)

    filename = "mistral-7b-instruct-v0.2.Q3_K_L.gguf"
    local_path = os.path.join(target_dir, filename)

    if not os.path.exists(local_path):
        print("Downloading model...")
        downloaded_path = hf_hub_download(
            repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
            filename=filename,
            cache_dir=target_dir,
        )
        # Move from cache to final destination (optional)
        if downloaded_path != local_path:
            os.rename(downloaded_path, local_path)
    else:
        print(f"Model already exists at: {local_path}")


def compute_matches(vector_store, query_str_embedding, top_k=3):
    """
    This function takes in a vector store dictionary, a query string, and an int 'top_k'.
    It computes embeddings for the query string and then calculates the cosine similarity against every chunk embedding in the dictionary.
    The top_k matches are returned based on the highest similarity scores.
    """
    # Get the embedding for the query string
    scores = {}

    # Calculate the cosine similarity between the query embedding and each chunk's embedding
    for chunk_id, chunk_embedding in vector_store.items():
        chunk_embedding_array = np.array(chunk_embedding)
        # Normalize embeddings to unit vectors for cosine similarity calculation
        norm_query = np.linalg.norm(query_str_embedding)
        norm_chunk = np.linalg.norm(chunk_embedding_array)
        if norm_query == 0 or norm_chunk == 0:
            # Avoid division by zero
            score = 0
        else:
            score = np.dot(chunk_embedding_array, query_str_embedding) / (
                norm_query * norm_chunk
            )
        # Store the score along with a reference to both the document and the chunk
        scores[(chunk_id, chunk_id)] = score

    # Sort scores and return the top_k results
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)[
        :top_k
    ]
    top_results = [
        (doc_id, chunk_id, score) for ((doc_id, chunk_id), score) in sorted_scores
    ]

    return top_results


def load_paragraphs_from_folder(folder="TestData"):
    docs = []
    file_names = []
    folder_path = Path(folder)
    for file_path in folder_path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            docs.extend(paragraphs)
            file_names.extend([file_path.name] * len(paragraphs))
    return docs, file_names

def print_rag_param(rag_param):

    print("Chunk Size:", rag_param["chunk_size"])
    print("Model types:", rag_param["document_types"])
    print("Embedding model:", rag_param["embedding_model"])
    print("LLM model:", rag_param["llm_model"])