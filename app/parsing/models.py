from pydantic import BaseModel
from typing import List, Optional


class ContentBlock(BaseModel):

    block_id: str

    content: str

    content_type: str
    # text / heading / table / code / image

    heading_level: Optional[int] = None

    page_number: Optional[int] = None

    parent_section: Optional[str] = None


class StructuredDocument(BaseModel):

    doc_id: str

    source_path: str

    blocks: List[ContentBlock]