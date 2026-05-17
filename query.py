from app.core.env_validator import EnvValidator
from app.core.logger import logger

from app.indexing.hybrid_indexer import HybridIndexer
from app.retrieval.retrieval_pipeline import RetrievalPipeline
from app.retrieval.reranker import CohereReranker
from app.generation.generation_pipeline import GenerationPipeline

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

def run_query_service():
    console = Console()

    logger.info("Starting QUERY SERVICE...")

    indexer = HybridIndexer()

    # IMPORTANT:
    # Load existing Chroma + BM25 state
    # rebuild BM25 from Chroma-stored memory (simple approach)
    all_chunks = indexer.chroma.collection.get(include=["documents", "metadatas"])

    chunks = []

    for i in range(len(all_chunks["ids"])):
        chunks.append({
            "chunk_id": all_chunks["ids"][i],
            "content": all_chunks["documents"][i],
            "metadata": all_chunks["metadatas"][i]
        })

    indexer.load_existing_index(chunks)

    reranker = CohereReranker()

    retrieval_pipeline = RetrievalPipeline(
        chroma_collection=indexer.chroma.collection,
        bm25_indexer=indexer.bm25,
        reranker=reranker,
        all_chunks=indexer.all_chunks
    )

    generator = GenerationPipeline()

    while True:

        console.print(
            Panel.fit(
                "[bold cyan]Enter your query below[/bold cyan]",
                title="QUERY INPUT",
                border_style="cyan"
            )
        )

        query = console.input(
            "[bold yellow]> [/bold yellow]"
        ).strip()
        
        if query.lower() == "exit":

            logger.info("Shutting down QUERY SERVICE")
            break

        logger.info(f"Query: {query}")

        retrieval_result = retrieval_pipeline.retrieve(query)

        context = retrieval_result["context"]

        retrieved_chunks = retrieval_result["retrieved_chunks"]
        
        response = generator.generate(
            query=query,
            context=context,
            retrieved_chunks=retrieved_chunks
        )

        console.print()

        console.print(
            Panel.fit(
                f"[bold yellow]{query}[/bold yellow]",
                title="QUERY",
                border_style="cyan"
            )
        )

        console.print()

        console.print(
            Panel(
                Markdown(response),
                title="ANSWER",
                border_style="green"
            )
        )


if __name__ == "__main__":

    try:

        EnvValidator.validate()

        run_query_service()

    except Exception as e:

        logger.error(f"Query service failed: {str(e)}")