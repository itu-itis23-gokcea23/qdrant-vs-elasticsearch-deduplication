"""
load_elasticsearch.py
---------------------
Uploads complaints to Elasticsearch.
A 'category' field is added for each complaint — this represents a manually entered label.
There is NO semantic search in ES; only keyword-based search is available.
Used as a reference system for comparison with Qdrant.
"""

import json
from elasticsearch import Elasticsearch, helpers
from rich.console import Console

# Initialize rich console for styled terminal output
console = Console()

# Configuration constants
INDEX_NAME = "complaints"
ES_HOST = "http://localhost:9200"


def load_complaints(path="data/complaints.json"):
    """Reads the generated complaints from the JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    console.rule("[bold red]Elasticsearch Loading Process Started")

    # 1. Load complaints from local JSON
    complaints = load_complaints()
    console.print(f"[green]✅ {len(complaints)} complaints loaded from file[/green]")

    # 2. Establish connection to Elasticsearch server
    es = Elasticsearch(ES_HOST)
    if not es.ping():
        console.print("[bold red]❌ Could not connect to Elasticsearch! Is Docker running?[/bold red]")
        return
    console.print(f"[green]✅ Elasticsearch connection established[/green]")

    # 3. Index management: delete if it already exists to ensure a clean start
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        console.print(f"[yellow]♻️  Existing index deleted[/yellow]")

    # 4. Create the index with specific mappings for keyword and text search
    es.indices.create(
        index=INDEX_NAME,
        body={
            "mappings": {
                "properties": {
                    "id":       {"type": "integer"},
                    "text":     {"type": "text", "analyzer": "standard"},
                    "category": {"type": "keyword"},
                }
            }
        },
    )
    console.print(f"[green]✅ Index created: '{INDEX_NAME}'[/green]")

    # 5. Prepare and execute bulk upload (ingestion)
    actions = [
        {
            "_index": INDEX_NAME,
            "_id": c["id"],
            "_source": {
                "id": c["id"],
                "text": c["text"],
                "category": c["category"],
            },
        }
        for c in complaints
    ]

    # Perform high-performance bulk indexing
    success, failed = helpers.bulk(es, actions, raise_on_error=False)
    # Refresh the index to make the data immediately searchable
    es.indices.refresh(index=INDEX_NAME)

    console.print(f"[bold green]🚀 {success} complaints successfully uploaded to Elasticsearch![/bold green]")
    if failed:
        console.print(f"[red]⚠️  {len(failed)} records failed to upload[/red]")

    # 6. Verification check: Verify the number of indexed documents
    count = es.count(index=INDEX_NAME)["count"]
    console.print(f"[cyan]📊 Index status: {count} documents indexed[/cyan]")


if __name__ == "__main__":
    main()