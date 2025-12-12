import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

# Initialize Chroma Client (Persistent)
# This creates a folder 'chroma_db' in the project root
client = chromadb.PersistentClient(path="./chroma_db")

# Use OpenAI Embedding Function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

# Create or Get Collection
def get_transaction_collection():
    return client.get_or_create_collection(
        name="financial_transactions",
        embedding_function=openai_ef
    )
