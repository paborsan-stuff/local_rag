import yaml
from pathlib import Path

def load_env():

    env_path = Path ('env/config.yaml')
    with open(env_path, 'r') as file:
        config = yaml.safe_load(file)
    # Use .get() with an empty dictionary as default for robustness

    print ("Model name", config["model_name"])



def main():
    

    load_env()
    ##Creates text chunk based on tokens for processing
    #docs = chunker.document_chunker(directory_path='/home/paborsan/Documents/RAG_Data',
    #                        model_name='BAAI/bge-small-en-v1.5',
    #                        chunk_size=256)
    #
    #vec_store = indexer.create_vector_store(docs)
    #
    #matches = indexer.Indexer.compute_matches(vector_store=vec_store,
    #            query_str="Pablo",
    #            top_k=3)
    #print(matches)
    
if __name__ == "__main__":
    main()