import os
from modules import chunker, indexer


def main():
    
    #Creates text chunk based on tokens for processing
    docs = chunker.document_chunker(directory_path=os.path.expanduser(),
                            model_name='mistralai/Mistral-7B-Instruct-v0.2',
                            chunk_size=256)
    
    vec_store = indexer.create_vector_store(docs)

    matches = indexer.Indexer.compute_matches(vector_store=vec_store,
                query_str="Pablo",
                top_k=3)
    print(matches)
    
if __name__ == "__main__":
    main()