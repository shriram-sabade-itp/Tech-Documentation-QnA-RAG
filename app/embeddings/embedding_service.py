from sentence_transformers import (
    SentenceTransformer
)

from app.embeddings.embedding_models import (
    EmbeddedChunk
)

from app.embeddings.embedding_cache import (
    EmbeddingCache
)

from app.embeddings.vector_utils import (
    normalize_vector
)

from app.embeddings.batching import (
    create_batches
)

from app.core.logger import logger

class EmbeddingService:

    def __init__(self, model_name="all-MiniLM-L6-v2", batch_size=16):
        logger.info(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size
        self.cache = EmbeddingCache()

    @staticmethod
    def build_metadata(chunk):

        return {

            "global_id":
                f"{chunk.doc_id}:{chunk.chunk_id}",

            "doc_id":
                chunk.doc_id,

            "chunk_id":
                chunk.chunk_id,

            "section_id":
                chunk.section_id,

            "chunk_level":
                chunk.chunk_level,

            "checksum":
                chunk.checksum,

            # IMPORTANT
            "source_path":
                chunk.source_path,

            "heading_h1":
                chunk.heading_h1,

            "heading_h2":
                chunk.heading_h2,

            "heading_h3":
                chunk.heading_h3
        }

    def embed_chunks(self, enriched_chunks):

        embedded_chunks = []
        batches = create_batches(enriched_chunks, self.batch_size)

        for batch in batches:

            texts_to_embed = []
            uncached_chunks = []

            # STEP 1: cache check
            for chunk in batch:

                if self.cache.exists(chunk.checksum):

                    embedding = self.cache.get(chunk.checksum)

                    embedded_chunks.append(
                        EmbeddedChunk(
                            chunk_id=chunk.chunk_id,
                            doc_id=chunk.doc_id,
                            content=chunk.content,
                            embedding=embedding,
                            metadata=self.build_metadata(chunk)
                        )
                    )

                else:
                    texts_to_embed.append(chunk.content)
                    uncached_chunks.append(chunk)

            # STEP 2: embedding
            if texts_to_embed:

                vectors = self.model.encode(
                    texts_to_embed,
                    convert_to_numpy=True
                )

                # STEP 3: normalize + cache
                for chunk, vector in zip(uncached_chunks, vectors):

                    normalized_vector = normalize_vector(vector).tolist()

                    self.cache.set(chunk.checksum, normalized_vector)

                    embedded_chunks.append(
                        EmbeddedChunk(
                            chunk_id=chunk.chunk_id,
                            doc_id=chunk.doc_id,
                            content=chunk.content,
                            embedding=normalized_vector,
                            metadata=self.build_metadata(chunk)
                        )
                    )

        logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks")

        return embedded_chunks