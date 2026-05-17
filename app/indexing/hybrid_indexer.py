from app.indexing.chroma_manager import ChromaManager
from app.indexing.bm25_indexer import BM25Indexer
from app.core.logger import logger
from app.embeddings.embedding_models import EmbeddedChunk
from app.core.chunk_mapper import ChunkMapper

class HybridIndexer:

    def __init__(self):

        self.chroma = ChromaManager()
        self.bm25 = BM25Indexer()
        self.all_chunks: list[EmbeddedChunk] = []

    def index(self, embedded_chunks):

        logger.info("Starting hybrid indexing")

        # normalize EVERYTHING once
        self.all_chunks = [
            ChunkMapper.to_dict(c) for c in embedded_chunks
        ]

        self.chroma.upsert_chunks(embedded_chunks)
        self.bm25.build_index(embedded_chunks)

        logger.info("Hybrid indexing completed")

    def load_existing_index(self, embedded_chunks: list[EmbeddedChunk]):

        logger.info("Loading existing index...")

        self.chroma = ChromaManager()
        self.bm25 = BM25Indexer()

        self.bm25.build_index(embedded_chunks)

        self.all_chunks = embedded_chunks