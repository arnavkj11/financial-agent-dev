import chromadb
from app.core.config import settings
import os

def check_vector_db():
    start_path = os.getcwd()
    persist_dir = os.path.join(start_path, "chroma_db")
    
    print(f"Checking Vector DB at: {persist_dir}")
    
    if not os.path.exists(persist_dir):
        print("No chroma_db folder found.")
        return

    client = chromadb.PersistentClient(path=persist_dir)
    try:
        collection = client.get_collection("financial_transactions")
        count = collection.count()
        print(f"Total Embeddings in Vector DB: {count}")
        
        # Peek at results for Netflix
        results = collection.query(
            query_texts=["Netflix"],
            n_results=10
        )
        
        print("\n--- Search Results for 'Netflix' ---")
        for i, doc in enumerate(results['documents'][0]):
            print(f"[{i}] {doc}")
            
    except Exception as e:
        print(f"Error reading collection: {e}")

if __name__ == "__main__":
    check_vector_db()
