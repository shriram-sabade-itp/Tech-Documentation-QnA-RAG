from rank_bm25 import BM25Okapi
from app.core.logger import logger

from app.core.chunk_mapper import ChunkMapper

class BM25Indexer:

    def build_index(self, embedded_chunks):

        logger.info("Building BM25 index")

        tokenized_docs = []

        self.documents = []
        self.chunks = []

        for chunk in embedded_chunks:

            c = ChunkMapper.to_dict(chunk)

            content = c["content"]

            tokens = content.split()

            tokenized_docs.append(tokens)

            self.documents.append(content)
            self.chunks.append(c)

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query, top_k=5):

        scores = self.bm25.get_scores(query.split())

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        results = []

        for idx, score in ranked[:top_k]:

            chunk = self.chunks[idx]

            results.append({
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "metadata": chunk["metadata"],
                "score": float(score),
                "retrieval_type": "bm25"
            })

        return results