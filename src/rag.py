from modules import chunker, indexer


def main():
    
    #Creates text chunk based on tokens for processing
    docs = chunker.document_chunker(directory_path='/home/paborsan/Documents/RAG_Data',
                            model_name='BAAI/bge-small-en-v1.5',
                            chunk_size=256)
    
    vec_store = indexer.create_vector_store(docs)

    matches = indexer.Indexer.compute_matches(vector_store=vec_store,
                query_str="Pablo",
                top_k=3)
    print(matches)
    
if __name__ == "__main__":
    main()