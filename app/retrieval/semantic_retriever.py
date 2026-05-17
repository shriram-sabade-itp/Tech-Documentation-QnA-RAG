from sentence_transformers import (
    SentenceTransformer
)

from app.embeddings.vector_utils import (
    normalize_vector
)

class SemanticRetriever:

    def __init__(self, chroma_collection):
        self.collection = chroma_collection
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve(self, query, top_k=20):

        query_vector = self.model.encode(query, convert_to_numpy=True)
        query_vector = normalize_vector(query_vector)

        results = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k
        )

        retrieved = []

        for i in range(len(results["ids"][0])):

            retrieved.append({
                "chunk_id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] or {},
                "score": results["distances"][0][i],
                "retrieval_type": "semantic"
            })

        return retrieved