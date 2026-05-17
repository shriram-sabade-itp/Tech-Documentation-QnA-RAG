from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RawDocument(BaseModel):
    doc_id: str
    file_name: str
    source_path: str
    file_size: int
    checksum: str
    version: str
    content: str
    created_at: datetime


class Checkpoint(BaseModel):
    doc_id: str
    status: str
    last_updated: datetime
    error_message: Optional[str] = None