import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel


class Indexer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model     = AutoModel.from_pretrained(model_name)
        self.tokenizer.save_pretrained("model/tokenizer")
        self.model.save_pretrained("model/embedding")

    def compute_embeddings(self, text):
        # aquí reutilizas los objetos que ya tienes
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        with torch.no_grad():
            emb = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()
        return emb.tolist()

    def create_vector_store(self, doc_store):
        vector_store = {}
        for doc_id, chunks in doc_store.items():
            doc_vectors = {}
            for chunk_id, chunk_dict in chunks.items():
                # llamas al método como self.compute_embeddings
                doc_vectors[chunk_id] = self.compute_embeddings(chunk_dict["text"])
            vector_store[doc_id] = doc_vectors
        return vector_store
    
    def compute_matches(self, vector_store, query_str, top_k):
        """
        This function takes in a vector store dictionary, a query string, and an int 'top_k'.
        It computes embeddings for the query string and then calculates the cosine similarity against every chunk embedding in the dictionary.
        The top_k matches are returned based on the highest similarity scores.
        """
        # Get the embedding for the query string
        query_str_embedding = np.array(self.compute_embeddings(query_str))
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