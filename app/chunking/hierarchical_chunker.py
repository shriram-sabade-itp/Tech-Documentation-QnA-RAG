import uuid

from app.chunking.models import Chunk
from app.chunking.token_counter import simple_token_count
from app.chunking.utils import sliding_window


class HierarchicalChunker:

    def __init__(self,
                 parent_chunk_size=300,
                 child_chunk_size=120,
                 overlap=30):

        self.parent_chunk_size = parent_chunk_size

        self.child_chunk_size = child_chunk_size

        self.overlap = overlap

    def chunk_document(self, structured_document):

        parent_chunks = []

        child_chunks = []

        order_index = 0

        current_heading = "ROOT"

        text_blocks = []

        # Step 1:
        # Convert blocks into section-aware text groups

        for block in structured_document.blocks:

            if block.content_type == "heading":

                current_heading = block.content

                continue

            text_blocks.append({
                "heading": current_heading,
                "content": block.content,
                "content_type": block.content_type
            })

        # Step 2:
        # Create parent chunks

        combined_text = []

        for block in text_blocks:

            combined_text.append(block["content"])

        words = " ".join(combined_text).split()

        for parent_window in sliding_window(
                words,
                self.parent_chunk_size,
                self.overlap):

            parent_text = " ".join(parent_window)

            parent_chunk_id = str(uuid.uuid4())

            parent_chunk = Chunk(
                chunk_id=parent_chunk_id,
                parent_chunk_id=None,
                doc_id=structured_document.doc_id,
                content=parent_text,
                content_type="text",
                chunk_level="parent",
                heading_path=current_heading,
                token_count=simple_token_count(parent_text),
                order_index=order_index
            )

            parent_chunks.append(parent_chunk)

            order_index += 1

            # Step 3:
            # Create child chunks

            child_words = parent_text.split()

            for child_window in sliding_window(
                    child_words,
                    self.child_chunk_size,
                    self.overlap):

                child_text = " ".join(child_window)

                child_chunk = Chunk(
                    chunk_id=str(uuid.uuid4()),
                    parent_chunk_id=parent_chunk_id,
                    doc_id=structured_document.doc_id,
                    content=child_text,
                    content_type="text",
                    chunk_level="child",
                    heading_path=current_heading,
                    token_count=simple_token_count(child_text),
                    order_index=order_index
                )

                child_chunks.append(child_chunk)

                order_index += 1

        return {
            "parent_chunks": parent_chunks,
            "child_chunks": child_chunks
        }