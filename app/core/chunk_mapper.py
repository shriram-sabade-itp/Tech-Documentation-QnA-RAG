from typing import Any, Dict


class ChunkMapper:

    @staticmethod
    def to_dict(chunk: Any) -> Dict:

        """
        Converts ANY chunk type into standard dict format
        Supports:
        - EmbeddedChunk (Pydantic)
        - EnrichedChunk (Pydantic)
        - dict (already normalized)
        """

        # CASE 1: already dict
        if isinstance(chunk, dict):
            return {
                "chunk_id": chunk.get("chunk_id"),
                "doc_id": chunk.get("doc_id"),
                "content": chunk.get("content"),
                "embedding": chunk.get("embedding"),
                "metadata": chunk.get("metadata", {})
            }

        # CASE 2: Pydantic v2
        if hasattr(chunk, "model_dump"):
            data = chunk.model_dump()
            return {
                "chunk_id": data.get("chunk_id"),
                "doc_id": data.get("doc_id"),
                "content": data.get("content"),
                "embedding": data.get("embedding"),
                "metadata": data.get("metadata", {})
            }

        # CASE 3: fallback object
        return {
            "chunk_id": getattr(chunk, "chunk_id", None),
            "doc_id": getattr(chunk, "doc_id", None),
            "content": getattr(chunk, "content", None),
            "embedding": getattr(chunk, "embedding", None),
            "metadata": getattr(chunk, "metadata", {})
        }