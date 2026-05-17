class BM25Retriever:

    def __init__(self, bm25_indexer):
        self.bm25_indexer = bm25_indexer

    def retrieve(self, query, top_k=20):

        results = self.bm25_indexer.search(
            query=query,
            top_k=top_k
        )

        formatted = []

        for result in results:

            formatted.append({
                "chunk_id": result["chunk_id"],
                "content": result["content"],
                "metadata": result.get("metadata", {}),
                "score": result["score"],
                "retrieval_type": "bm25"
            })

        return formatted