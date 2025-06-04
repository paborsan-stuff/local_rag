import yaml
from modules.Chunker import Chunker
from modules.EmbeddingGenerator import EmbeddingGenerator
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
import numpy as np

TEST_PARAGRAPHS = """Basement home theater seating in black leather, includes three reclining seats with cup holders and storage compartments.
Designed for ultimate comfort and convenience during movie nights. 

Manufactured by Luxe Seating. Dimensions per seat: 36"W x 40"D x 40"H.
"""

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

def compute_matches(vector_store, query_str, query_str_embedding, top_k):
    """
    This function takes in a vector store dictionary, a query string, and an int 'top_k'.
    It computes embeddings for the query string and then calculates the cosine similarity against every chunk embedding in the dictionary.
    The top_k matches are returned based on the highest similarity scores.
    """
    # Get the embedding for the query string
    query_str_embedding = 
    scores = {}

    # Calculate the cosine similarity between the query embedding and each chunk's embedding
    for doc_id, chunks in vector_store.items():
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

            # Store the score along with a reference to both the document and the chunk
            scores[(doc_id, chunk_id)] = score

    # Sort scores and return the top_k results
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
    top_results = [(doc_id, chunk_id, score) for ((doc_id, chunk_id), score) in sorted_scores]

    return top_results

def main():

    rag_param = load_env()

    print("Chunk Size", rag_param["chunk_size"])
    print("Model name", rag_param["model_name"])
    print("Model types", rag_param["document_types"])

    mdl_chunker = Chunker(rag_param["model_name"], input_text = TEST_PARAGRAPHS)

    tokenized_chunks = mdl_chunker.process_paragraphs()

    #print("tokenized_chunks", tokenized_chunks)

    model_name = "BAAI/bge-small-en-v1.5"

    fetch_text_emb_model(model_name)

    emb_mdl = EmbeddingGenerator ("tmp")

    vectorized_chunks = emb_mdl.create_vector_store(tokenized_chunks)

    #print("vectorized_chunks", vectorized_chunks)

    #np.array(compute_embeddings(query_str))

    #compute_matches ()

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
    #
    # print(matches)


if __name__ == "__main__":
    main()
