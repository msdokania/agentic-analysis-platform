from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from app.settings import QDRANT_URL
from app.settings import COLLECTION_NAME


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

client = QdrantClient(url=QDRANT_URL)

def get_vector_store() -> QdrantVectorStore:
    print("Getting vector store...")
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in collections:
        print("Creating collection...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE,
            ),
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )