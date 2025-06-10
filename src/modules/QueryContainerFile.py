from llama_cpp import Llama
from modules.LLMAdapter import LLMAdapter

def compute_get_vector_store(rag_param, emb_mdl, args, docs, file_names, doc_id_map):
    for doc, file_name in zip(docs, file_names):
        mdl_chunker = Chunker(rag_param["embedding_model"], input_text=doc)
        chunks = mdl_chunker.process_paragraphs()
        doc_id_map[file_name] = chunks
 
    vector_store = get_query_vector_store_db(emb_mdl, doc_id_map, args.use_cache)

    if not vector_store:
        raise ValueError("Empty Vector data base")
    return vector_store

def retrieval_llm_response(query_str):
    retrieved_docs = process_query_str(emb_mdl, doc_id_map, vector_store, query_str)

    # Prepare LLM prompt
    system_prompt = """
    You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
    Your job is to understand the request, and answer based on the retrieved context.
    """

    llm = Llama(model_path="./tmp/llm/mistral-7b-instruct-v0.2.Q3_K_L.gguf", n_gpu_layers=10)
    instance_model = LLMAdapter(llm)

    llm_prompt = LLMAdapter.construct_prompt(
        system_prompt=system_prompt,
        retrieved_docs=retrieved_docs,
        user_query=query_str
    )

    response = instance_model.stream_and_buffer_response(base_prompt=llm_prompt, max_tokens=800)
    print("LLM Response:", response)


def process_query_str(emb_mdl, doc_id_map, vector_store, query_str):
    query_str_embedding = np.array(emb_mdl.compute_embeddings(query_str))
    print(doc_id_map)

    top_score, middle_score, last_score = find_db_vector_best_dot_score(vector_store, query_str_embedding, top_k=3)
    retrieved_docs = doc_id_map[top_score[0]][top_score[1]]['text']
    print("Documento: ", top_score[0])
    print("Chunk: ", retrieved_docs)
    return retrieved_docs


def get_query_vector_store_db(emb_mdl, doc_id_map, use_cache):
    #vector_store = {}

    if use_cache == False:
        #vector_store = create_vector_store(emb_mdl, doc_id_map, vector_store)
        vector_store = emb_mdl.create_vector_store(doc_id_map)
        os.makedirs(os.path.dirname("vdb/vector_db.json"), exist_ok=True)
        with open('vdb/vector_db.json', 'w') as f:
            json.dump(vector_store, f)
    else: 
        with open('vdb/vector_db.json', 'r') as f:
            try:
                dbjson = json.load(f)
                if not dbjson:
                    #vector_store = create_vector_store(emb_mdl, doc_id_map, vector_store)
                    vector_store = emb_mdl.create_vector_store(doc_id_map)
                else:
                    print("Vector db file cached!")
                    vector_store = dbjson
            except json.JSONDecodeError:
                print(f"[ERROR] Invalid JSON format in vdb/vector_db.json ")
                return None
    return vector_store