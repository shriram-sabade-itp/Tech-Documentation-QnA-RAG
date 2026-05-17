import uuid

from app.parsing.base_parser import BaseParser
from app.parsing.models import StructuredDocument, ContentBlock


class TextParser(BaseParser):

    def parse(self, raw_document):

        blocks = []

        paragraphs = raw_document.content.split("\n\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            block = ContentBlock(
                block_id=str(uuid.uuid4()),
                content=paragraph,
                content_type="text"
            )

            blocks.append(block)

        return StructuredDocument(
            doc_id=raw_document.doc_id,
            source_path=raw_document.source_path,
            blocks=blocks
        )