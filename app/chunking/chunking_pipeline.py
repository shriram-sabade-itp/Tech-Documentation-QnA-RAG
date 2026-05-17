from app.core.logger import logger

from app.chunking.hierarchical_chunker import (
    HierarchicalChunker
)

from app.chunking.semantic_chunker import (
    SemanticChunker
)


class ChunkingPipeline:

    def __init__(self):

        self.hierarchical_chunker = (
            HierarchicalChunker()
        )

        self.semantic_chunker = (
            SemanticChunker()
        )

    def process(self, structured_document):

        logger.info("Starting chunking pipeline")

        chunks = self.hierarchical_chunker.chunk_document(
            structured_document
        )

        logger.info(
            f"Generated "
            f"{len(chunks['parent_chunks'])} parent chunks "
            f"and "
            f"{len(chunks['child_chunks'])} child chunks"
        )

        return chunks