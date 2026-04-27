"""
load_qdrant.py
--------------
Converts complaints into embeddings and uploads them to Qdrant.
Model: paraphrase-multilingual-MiniLM-L12-v2 (Supports Turkish, free to use)
"""

import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.progress import track

# Initialize rich console for styled terminal output
console = Console()

# Configuration constants
COLLECTION_NAME = "complaints"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333


def load_complaints(path="data/complaints.json"):
    """Reads the generated complaints from the JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    console.rule("[bold blue]Qdrant Loading Process Started")

    # 1. Load complaints from local JSON
    complaints = load_complaints()
    console.print(f"[green]✅ {len(complaints)} complaints loaded from file[/green]")

    # 2. Initialize the Sentence Transformer model
    console.print(f"[yellow]🔄 Loading model: {MODEL_NAME}[/yellow]")
    model = SentenceTransformer(MODEL_NAME)
    vector_size = model.get_sentence_embedding_dimension()
    console.print(f"[green]✅ Model ready — vector dimension: {vector_size}[/green]")

    # 3. Establish connection to Qdrant server
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    console.print(f"[green]✅ Qdrant connection established ({QDRANT_HOST}:{QDRANT_PORT})[/green]")

    # 4. Collection management: recreate if it already exists
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        console.print(f"[yellow]♻️  Existing collection deleted[/yellow]")

    # Create a new collection with Cosine similarity configuration
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    console.print(f"[green]✅ Collection created: '{COLLECTION_NAME}'[/green]")

    # 5. Generate embeddings and prepare points for upload
    texts = [c["text"] for c in complaints]
    console.print("[yellow]🔄 Generating embeddings...[/yellow]")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Wrap vectors and metadata (payload) into Qdrant PointStructs
    points = [
        PointStruct(
            id=c["id"],
            vector=embeddings[i].tolist(),
            payload={
                "text": c["text"],
                "category": c["category"],
            },
        )
        for i, c in enumerate(complaints)
    ]

    # Batch upload (upsert) to Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    console.print(f"[bold green]🚀 {len(points)} complaints successfully uploaded to Qdrant![/bold green]")

    # 6. Verification check
    info = client.get_collection(COLLECTION_NAME)
    console.print(f"[cyan]📊 Collection status: {info.points_count} points indexed[/cyan]")


if __name__ == "__main__":
    main()