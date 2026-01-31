from pathlib import Path
from app.vectorstore.client import get_vector_store
from app.vectorstore.loaders import load_pdf


def ingest_pdf(pdf_path: Path):
    vector_store = get_vector_store()
    print("Got vector store. Now adding doc...")
    chunks = load_pdf(pdf_path)
    vector_store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks from {pdf_path.name}")