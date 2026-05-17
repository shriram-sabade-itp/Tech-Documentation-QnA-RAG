from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EnrichedChunk(BaseModel):

    doc_id: str
    section_id: str
    chunk_id: str
    parent_chunk_id: Optional[str]

    source_path: str
    page_number: Optional[int]
    source_file: str
    
    heading_h1: Optional[str]
    heading_h2: Optional[str]
    heading_h3: Optional[str]

    content: str
    content_type: str
    chunk_level: str

    token_count: int

    embedding_model: str
    created_at: datetime
    version: str
    checksum: str

    lineage_path: str
    order_index: int

    class Config:
        frozen = True   