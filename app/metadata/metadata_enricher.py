from datetime import datetime

from app.metadata.metadata_models import EnrichedChunk
from app.metadata.checksum_utils import generate_chunk_checksum
from app.metadata.lineage_builder import build_lineage_path


class MetadataEnricher:

    def __init__(self):
        self.embedding_model = "all-MiniLM-L6-v2"

    def enrich(self, chunks, raw_document):

        enriched_chunks = []

        for chunk in (chunks["parent_chunks"] + chunks["child_chunks"]):

            checksum = generate_chunk_checksum(chunk.content)

            lineage_path = build_lineage_path(
                raw_document.doc_id,
                chunk.heading_path,
                chunk.chunk_id
            )

            enriched_chunks.append(
                EnrichedChunk(
                    doc_id=raw_document.doc_id,
                    section_id=chunk.heading_path,
                    chunk_id=f"{raw_document.doc_id}_{chunk.chunk_id}",
                    parent_chunk_id=chunk.parent_chunk_id,
                    source_path=raw_document.source_path,
                    source_file=raw_document.source_path,
                    page_number=None,

                    heading_h1=chunk.heading_path,
                    heading_h2=None,
                    heading_h3=None,

                    content=chunk.content,
                    content_type=chunk.content_type,
                    chunk_level=chunk.chunk_level,

                    token_count=chunk.token_count,

                    embedding_model=self.embedding_model,
                    created_at=datetime.utcnow(),
                    version=raw_document.version,

                    checksum=checksum,
                    lineage_path=lineage_path,
                    order_index=chunk.order_index
                )
            )

        return enriched_chunks
    
    