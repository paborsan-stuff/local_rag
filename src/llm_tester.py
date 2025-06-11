# from llama_cpp import Llama
# from modules.LLMAdapter import LLMAdapter
# from huggingface_hub import hf_hub_download
# import sys


# # Usage
# system_prompt = """
# You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.

# Your job is to understand the request, and answer based on the retrieved context.
# """

# retrieved_docs = """
# Un cine en casa es un sistema de entretenimiento en el hogar diseñado para recrear la experiencia y el ambiente de una sala de cine. Este sistema utiliza equipos de video y audio de alta calidad para ofrecer una experiencia visual y auditiva inmersiva. 
# Elementos clave de un cine en casa:

#     Pantalla:
#     Puede ser una televisión de gran tamaño o un proyector con pantalla de proyección. 

#     Cines en casa sencillos:
#     Pueden incluir una televisión de gran tamaño y un sistema de sonido envolvente, como una barra de sonido. 

# Cines en casa avanzados:
# Incluyen proyectores, pantallas de proyección, sistemas de audio de alta gama y control remoto. 
# Cines en casa de alta gama:
# Ofrecen una experiencia de cine personalizada con diseño de sala, iluminación, asientos y otros elementos que mejoran la experiencia
# """

# # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# llm = Llama(
#   model_path="/home/paborsan/Documents/Projects/local_rag/local_rag/src/tmp/llm/models--TheBloke--Mistral-7B-Instruct-v0.2-GGUF/blobs/2c0e37f9d639e349c31dbc3c365fc1a140339a43fe478702511f6efead15488a",  # Download the model file first
#   n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
#   n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
#   n_gpu_layers=35         # The number of layers to offload to GPU, if you have GPU acceleration available
# )

# instance_model = LLMAdapter(llm)

# llm_prompt = LLMAdapter.construct_prompt(system_prompt=system_prompt,
#                           retrieved_docs=retrieved_docs,
#                           user_query="Hola explicame que es un hogar de cine en casa y como se usa")



# response = instance_model.stream_and_buffer_response(base_prompt = llm_prompt, max_tokens = 1200)

# print (response)


from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import os

# Función simple que hace streaming y devuelve la respuesta completa
def generate_response(llm, prompt, max_tokens=1200):
    buffer = ""
    for output in llm(prompt, max_tokens=max_tokens, stream=True):
        token = output["choices"][0]["text"]
        print(token, end="", flush=True)  # opcional: mostrar en vivo
        buffer += token
    return buffer

# --- tu código original ---

# 1. Descarga del modelo (sin usar symlinks)
model_path = hf_hub_download(
    repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    filename="mistral-7b-instruct-v0.2.Q3_K_L.gguf",
    local_dir="tmp/llm",
    local_dir_use_symlinks=False
)

# 2. Inicializa Llama
llm = Llama(
    model_path=model_path,
    n_ctx=32768,
    n_threads=8,
    n_gpu_layers=35
)

# 3. Define tus prompts
system_prompt = """
You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.

Your job is to understand the request, and answer based on the retrieved context.
"""

retrieved_docs = """
Un cine en casa es un sistema de entretenimiento en el hogar diseñado para recrear la experiencia y el ambiente de una sala de cine...
"""

user_query = "Hola, explícame qué es un cine en casa y cómo se usa"

# 4. Construye el prompt final
full_prompt = (
    system_prompt.strip()
    + "\n\nContexto:\n" + retrieved_docs.strip()
    + "\n\nUsuario: " + user_query
    + "\nAsistente:"
)

# 5. Llama a la función y captura la respuesta
response = generate_response(llm, full_prompt, max_tokens=1200)

print("\n\nRespuesta completa:\n", response)