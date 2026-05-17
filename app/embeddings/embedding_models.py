from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EmbeddedChunk:

    chunk_id: str
    doc_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
