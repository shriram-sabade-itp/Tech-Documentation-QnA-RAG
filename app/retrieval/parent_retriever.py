class ParentRetriever:

    def expand(self, retrieved_chunks, all_chunks):

        expanded = []

        parent_lookup = {
            chunk["chunk_id"]: chunk
            for chunk in all_chunks
        }

        for result in retrieved_chunks:

            expanded.append(result)

            metadata = result.get("metadata", {})
            parent_id = metadata.get("parent_chunk_id")

            if parent_id and parent_id in parent_lookup:

                parent_chunk = parent_lookup[parent_id]

                expanded.append({
                    "chunk_id": parent_chunk["chunk_id"],
                    "content": parent_chunk["content"],
                    "metadata": parent_chunk.get("metadata", {}),
                    "retrieval_type": "parent"
                })

        return expanded