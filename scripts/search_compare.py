"""
search_compare.py
-----------------
MAIN DEMO SCRIPT

Sends the same query to both Elasticsearch and Qdrant and displays the results side-by-side.

Elasticsearch -> Keyword matching (standard search)
Qdrant        -> Semantic similarity (vector search)

Usage:
    python scripts/search_compare.py
    python scripts/search_compare.py --query "my product arrived very late"
"""

import argparse
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from elasticsearch import Elasticsearch
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

# Initialize rich console for professional terminal output
console = Console()

# Configuration constants
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "complaints"
INDEX_NAME = "complaints"
TOP_K = 5

# Predefined demo queries — ideal for the presentation slides
DEMO_QUERIES = [
    "the product packaging was damaged when opened",      # Expected category: kirik_urun
    "delivery date was way too late",                     # Expected category: gec_teslimat
    "they sent me something wrong",                       # Expected category: yanlis_urun
    "a dirty product came out of the box",                # Expected category: kirli_urun
    "refund never reached my account",                    # Expected category: iade_sorunu
    "the person at the support line was indifferent",     # Expected category: musteri_hizmetleri
]


def search_elasticsearch(es: Elasticsearch, query: str, top_k: int = TOP_K):
    """Performs standard keyword search in Elasticsearch."""
    result = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "match": {
                    "text": {
                        "query": query,
                        "operator": "or",
                    }
                }
            },
            "size": top_k,
        },
    )
    hits = result["hits"]["hits"]
    return [
        {
            "text": h["_source"]["text"],
            "category": h["_source"]["category"],
            "score": round(h["_score"], 3),
        }
        for h in hits
    ]


def search_qdrant(client: QdrantClient, model: SentenceTransformer, query: str, top_k: int = TOP_K):
    """Performs semantic/vector search in Qdrant."""
    # Convert input text to a numerical vector using the AI model
    query_vector = model.encode(query).tolist()
    
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )
    return [
        {
            "text": r.payload["text"],
            "category": r.payload["category"],
            "score": round(r.score, 3),
        }
        for r in results
    ]


def print_comparison(query: str, es_results: list, qdrant_results: list):
    """Displays search results in a side-by-side comparative table."""
    console.print()
    console.print(Panel(f'[bold white]Query:[/bold white] "{query}"', style="cyan"))

    # Construct Elasticsearch Results Table
    es_table = Table(
        title="🔍 Elasticsearch — Keyword Search",
        box=box.ROUNDED,
        style="red",
        header_style="bold red",
        show_lines=True,
    )
    es_table.add_column("Score", width=7)
    es_table.add_column("Category", width=20)
    es_table.add_column("Complaint Text")

    if es_results:
        for r in es_results:
            es_table.add_row(str(r["score"]), r["category"], r["text"])
    else:
        es_table.add_row("—", "—", "[italic]No results found[/italic]")

    # Construct Qdrant Results Table
    qdrant_table = Table(
        title="🧠 Qdrant — Semantic Search",
        box=box.ROUNDED,
        style="green",
        header_style="bold green",
        show_lines=True,
    )
    qdrant_table.add_column("Score", width=7)
    qdrant_table.add_column("Category", width=20)
    qdrant_table.add_column("Complaint Text")

    for r in qdrant_results:
        qdrant_table.add_row(str(r["score"]), r["category"], r["text"])

    # Render tables
    console.print(es_table)
    console.print(qdrant_table)

    # Summary logic for the demo
    if es_results:
        es_cats = set(r["category"] for r in es_results)
        q_cats  = set(r["category"] for r in qdrant_results)
        console.print(f"  [red]ES found categories:[/red]     {es_cats}")
        console.print(f"  [green]Qdrant found categories:[/green]  {q_cats}")
    else:
        console.print(f"  [red]ES:[/red] Returned zero results — the keywords are missing in the text!")
        q_cats = set(r["category"] for r in qdrant_results)
        console.print(f"  [green]Qdrant:[/green] Successfully found semantic matches for {q_cats} ✅")
    console.print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default=None, help="Run a single custom query")
    parser.add_argument("--all",   action="store_true",    help="Run all predefined demo queries")
    args = parser.parse_args()

    console.rule("[bold cyan]Elasticsearch vs Qdrant — Semantic Comparison Demo")

    # Connect to services
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        console.print("[bold red]❌ Could not connect to Elasticsearch![/bold red]")
        return

    client = QdrantClient(host="localhost", port=6333)

    # Load the embedding model locally
    console.print("[yellow]🔄 Loading embedding model...[/yellow]")
    model = SentenceTransformer(MODEL_NAME)
    console.print("[green]✅ Model ready[/green]")

    # Determine which queries to run
    if args.query:
        queries = [args.query]
    elif args.all:
        queries = DEMO_QUERIES
    else:
        # Default: show the first 3 demo queries
        queries = DEMO_QUERIES[:3]

    # Execute and compare
    for query in queries:
        es_results     = search_elasticsearch(es, query)
        qdrant_results = search_qdrant(client, model, query)
        print_comparison(query, es_results, qdrant_results)

    console.rule("[bold cyan]Demo Completed")
    console.print()
    console.print("[bold]CLI Commands:[/bold]")
    console.print("  Run all queries  : python scripts/search_compare.py --all")
    console.print('  Custom query     : python scripts/search_compare.py --query "bad packaging"')


if __name__ == "__main__":
    main()