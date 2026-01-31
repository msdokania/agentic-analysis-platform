import uvicorn
from pathlib import Path
from app.server import app
from app.vectorstore.ingest import ingest_pdf

def bootstrap_docs():
    print("Bootstrapping docs...")
    ingest_pdf(Path("data/aws-eks.pdf"))
    print("Bootstrapping done")
    # ingest_pdf(Path("data/networking-basics.pdf"))

if __name__ == "__main__":
    print("🔥 Starting app")
    # Uncomment below line when running for first time
    # bootstrap_docs()
    print("🌐 Starting Uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")