from rich.console import Console
from rich.panel import Panel

from app.core.env_validator import EnvValidator
from app.core.logger import logger

from app.ingestion.ingestion_pipeline import (
    IngestionPipeline
)

from app.indexing.hybrid_indexer import (
    HybridIndexer
)


console = Console()


# ==========================================
# UI HELPERS
# ==========================================

def show_error(message):

    console.print(
        Panel(
            f"[bold red]{message}[/bold red]",
            title="ERROR",
            border_style="red"
        )
    )


def show_warning(message):

    console.print(
        Panel(
            f"[bold yellow]{message}[/bold yellow]",
            title="WARNING",
            border_style="yellow"
        )
    )


def show_success(files_count,
                 chunks_count,
                 file_names):

    formatted_files = "\n".join(
        f"• {name}"
        for name in file_names
    )

    console.print(
        Panel.fit(
            f"""
[bold green]Ingestion Completed[/bold green]

Files Successfully Processed:
{files_count}

Successful Files:
{formatted_files}

Chunks Generated:
{chunks_count}
""",
            title="INGESTION SUCCESS",
            border_style="green"
        )
    )


# ==========================================
# MAIN LOOP
# ==========================================

def run_ingestion_loop():

    logger.info(
        "Starting INGESTION SERVICE..."
    )

    pipeline = IngestionPipeline()

    indexer = HybridIndexer()

    # IMPORTANT:
    # Keep cumulative chunks
    cumulative_chunks = []

    while True:

        console.print()

        console.print(
            Panel.fit(
                "[bold cyan]Enter file paths "
                "(comma separated) or type 'exit'[/bold cyan]",
                title="FILE INPUT",
                border_style="cyan"
            )
        )

        user_input = console.input(
            "[bold yellow]> [/bold yellow]"
        ).strip()

        # ==========================================
        # EXIT
        # ==========================================

        if user_input.lower() == "exit":

            logger.info(
                "Shutting down ingestion service"
            )

            console.print(
                Panel.fit(
                    "[bold green]Ingestion service stopped[/bold green]",
                    border_style="green"
                )
            )

            break

        # ==========================================
        # EMPTY INPUT
        # ==========================================

        if not user_input:

            show_error(
                "No files provided."
            )

            continue

        # ==========================================
        # PARSE FILES
        # ==========================================

        files = [

            file.strip()

            for file in user_input.split(",")

            if file.strip()
        ]

        # ==========================================
        # INGEST
        # ==========================================

        result = pipeline.ingest(files)

        # Safety fallback
        if not result:

            show_error(
                "Ingestion failed."
            )

            continue

        embedded_chunks = (
            result.get("embedded_chunks", [])
        )

        successful_files = (
            result.get("successful_files", 0)
        )

        successful_file_names = (
            result.get("successful_file_names", [])
        )

        empty_chunk_files = (
            result.get("empty_chunk_files", [])
        )

        failed_files = (
            result.get("failed_files", [])
        )

        warning_files = (
            result.get("warning_files", [])
        )

        # ==========================================
        # SHOW WARNINGS
        # ==========================================

        if warning_files:

            show_warning(
                "\n".join(warning_files)
            )
        
        # ==========================================
        # EMPTY CHUNK FILES
        # ==========================================

        if empty_chunk_files:

            show_warning(
                "No chunks generated for:\n\n"
                + "\n".join(
                    f"• {file}"
                    for file in empty_chunk_files
                )
            )

        # ==========================================
        # SHOW ERRORS
        # ==========================================

        if failed_files:

            show_error(
                "\n".join(failed_files)
            )

        # ==========================================
        # NO CHUNKS
        # ==========================================

        if not embedded_chunks:

            show_warning(
                "No chunks generated."
            )

            continue

        # ==========================================
        # CUMULATIVE INDEXING
        # ==========================================

        cumulative_chunks.extend(
            embedded_chunks
        )

        logger.info(
            "Building indexes..."
        )

        indexer.index(
            cumulative_chunks
        )

        # ==========================================
        # SUCCESS UI
        # ==========================================

        show_success(
            successful_files,
            len(embedded_chunks),
            successful_file_names
        )


# ==========================================
# ENTRYPOINT
# ==========================================

if __name__ == "__main__":

    try:

        EnvValidator.validate()

        run_ingestion_loop()

    except Exception as error:

        logger.error(
            f"Ingestion service failed: {str(error)}"
        )

        show_error(str(error))