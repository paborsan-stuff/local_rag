import os
import uuid
from transformers import AutoTokenizer, AutoModel
import torch # Assuming you have PyTorch installed for model operations

# --- EmbeddingGenerator Class ---
class EmbeddingGenerator:
    """
    A class to handle loading the embedding model and tokenizer,
    and computing embeddings for text chunks.
    """
    def __init__(self, model_path: str):
        """
        Initializes the EmbeddingGenerator by loading the tokenizer and model.

        Args:
            model_path (str): The path to the directory containing the tokenizer
                              and embedding model (e.g., "/model").
                              Assumes tokenizer is in "{model_path}/tokenizer"
                              and model is in "{model_path}/embedding".
        """
        try:
            # Load tokenizer from the specified path
            self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(model_path, "tokenizer"))
            # Load the embedding model from the specified path
            self.model = AutoModel.from_pretrained(os.path.join(model_path, "embedding"))
            # Set the model to evaluation mode (important for inference)
            #self.model.eval()
            #print(f"Successfully loaded tokenizer and model from: {model_path}")

        except Exception as e:
            print(f"Error loading model or tokenizer from '{model_path}': {e}")
            print("Please ensure the paths are correct and the model files exist.")
            raise # Re-raise the exception to stop if loading fails

    def compute_embeddings(self, text: str):
        """
        Computes the embeddings for a given text string.

        Args:
            text (str): The input text to embed.

        Returns:
            list: A list of floats representing the embedding vector.
        """
        # Prepare inputs for the model
        # padding=True: Pads sequences to the longest sequence in the batch
        # truncation=True: Truncates sequences to the model's maximum input length
        # return_tensors="pt": Returns PyTorch tensors
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Generate the embeddings without computing gradients (for inference)
        with torch.no_grad():
            # Pass inputs to the model. `last_hidden_state` contains the embeddings for each token.
            # `.mean(dim=1)` takes the average of token embeddings to get a single sentence embedding.
            # `.squeeze()` removes any singleton dimensions.
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()

        # Convert the PyTorch tensor to a Python list of floats
        return embeddings.tolist()

    def create_vector_store(self, doc_id_map):
    #def create_vector_store(self, token_chunks):
        """
        Creates a simple in-memory vector store from a document store.
        Each chunk's text is converted into an embedding.

        Args:
            doc_store (dict): A dictionary where keys are document IDs and values
                              are dictionaries of chunks (chunk_id: {"text": ..., "metadata": ...}).

        Returns:
            dict: A dictionary representing the vector store (doc_id: {chunk_id: embedding_vector}).
        """
        vector_store = {}

        for doc_id, chunks in doc_id_map.items():
                        
            embedding_result = {}

            for chunk_id, chunk_dict in chunks.items():
                # Generate an embedding for each chunk of text using the instance's method
                embedding_result[chunk_id] = self.compute_embeddings(chunk_dict.get("text"))

            vector_store[doc_id] = embedding_result

        return vector_store
