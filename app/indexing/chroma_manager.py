import chromadb

from app.core.logger import logger


class ChromaManager:

    def __init__(self,
                 collection_name="rag_collection"):

        logger.info("Initializing ChromaDB")

        self.client = chromadb.PersistentClient(
            path="./chroma_storage"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def sanitize_metadata(self, metadata):

        """
        Convert unsupported metadata
        types into Chroma-safe values.
        """

        sanitized = {}

        for key, value in metadata.items():

            # Convert datetime to string
            if hasattr(value, "isoformat"):

                sanitized[key] = value.isoformat()

            # Keep supported types
            elif isinstance(
                value,
                (str, int, float, bool)
            ) or value is None:

                sanitized[key] = value

            # Convert everything else to string
            else:

                sanitized[key] = str(value)

        return sanitized

    def upsert_chunks(self, embedded_chunks):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            ids.append(chunk.chunk_id)
            documents.append(chunk.content)
            embeddings.append(chunk.embedding)

            # 🔥 IMPORTANT: ensure pure dict
            metadata = dict(chunk.metadata)

            metadatas.append(
                self.sanitize_metadata(metadata)
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        logger.info(
            f"Upserted {len(ids)} chunks into ChromaDB"
        )