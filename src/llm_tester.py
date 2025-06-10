from llama_cpp import Llama
from modules.LLMAdapter import LLMAdapter
from huggingface_hub import hf_hub_download
import sys


# Usage
system_prompt = """
You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.

Your job is to understand the request, and answer based on the retrieved context.
"""

retrieved_docs = """
Wall-mounted electric fireplace with realistic LED flames and heat settings. Features a black glass frame and remote control for easy operation. Ideal for adding warmth and ambiance. Manufactured by Hearth & Home. Dimensions: 50"W x 6"D x 21"H.
"""


llm = Llama(model_path="tmp/llm/mistral-7b-instruct-v0.2.Q3_K_L.gguf", n_gpu_layers=1)
instance_model = LLMAdapter(llm)

llm_prompt = LLMAdapter.construct_prompt(system_prompt=system_prompt,
                          retrieved_docs=retrieved_docs,
                          user_query="Hola explicame que es un hogar de cine en casa y como se usa")

response = instance_model.stream_and_buffer_response(base_prompt = llm_prompt, max_tokens = 800)

print (response)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
        llm = Llama(model_path=model_path, n_gpu_layers=1)
        instance_model = LLMAdapter(llm)
        print(f"LLM model loaded from {model_path}")
    else:
        print("Usage: python llm_tester.py <path_to_llm_model>")