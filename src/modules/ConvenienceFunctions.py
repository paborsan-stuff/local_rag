import numpy as np
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
import yaml
import os

class Convenience:

    def __init__(self, cache_dir):

        self.cache_dir = cache_dir
                 
    def load_env(self):

        yaml_path = self.cache_dir + "/env/config.yaml"
        env_path = Path(yaml_path)
        with open(env_path, "r") as file:
            config = yaml.safe_load(file)
        # Use .get() with an empty dictionary as default for robustness
        return config


    def fetch_text_emb_model(self, model_name):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        tokenizer_path = self.cache_dir + "/tmp/tokenizer"
        model_path = self.cache_dir + "/tmp/embedding"

        tokenizer.save_pretrained(tokenizer_path)
        model.save_pretrained(model_path)


    def fetch_llm_model(self):

        # Target directory and model info
        target_dir = self.cache_dir + "/tmp/llm"
        os.makedirs(target_dir, exist_ok=True)

        filename = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        local_path = os.path.join(target_dir, filename)

        if not os.path.exists(local_path):
            print("Downloading model...")
            downloaded_path = hf_hub_download(
                repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                filename=filename,
                cache_dir=target_dir,
            )
            # Move from cache to final destination (optional)
            # if downloaded_path != local_path:
            #     os.rename(downloaded_path, local_path)
        else:
            print(f"Model already exists at: {local_path}")


    def load_paragraphs_from_folder(self, folder="TestData"):
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

    def print_rag_param(self, rag_param):

        print("Chunk Size:", rag_param["chunk_size"])
        print("Model types:", rag_param["document_types"])
        print("Embedding model:", rag_param["embedding_model"])
        print("LLM model:", rag_param["llm_model"])