from pydantic import BaseModel
from typing import Optional


class Chunk(BaseModel):

    chunk_id: str

    parent_chunk_id: Optional[str]

    doc_id: str

    content: str

    content_type: str

    chunk_level: str
    # parent / child

    heading_path: str

    token_count: int

    order_index: int