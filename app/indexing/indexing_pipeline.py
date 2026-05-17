from app.indexing.hybrid_indexer import (
    HybridIndexer
)

from app.core.logger import logger


class IndexingPipeline:

    def __init__(self):

        self.indexer = HybridIndexer()

    def process(self, embedded_chunks):

        logger.info(
            "Starting indexing pipeline"
        )

        self.indexer.index(
            embedded_chunks
        )

        logger.info(
            "Indexing pipeline completed"
        )