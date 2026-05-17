import uuid

from markdown_it import MarkdownIt

from app.parsing.base_parser import BaseParser
from app.parsing.models import StructuredDocument, ContentBlock


class MarkdownParser(BaseParser):

    def __init__(self):

        self.md = MarkdownIt()

    def parse(self, raw_document):

        tokens = self.md.parse(raw_document.content)

        blocks = []

        current_heading = None

        for token in tokens:

            if token.type == "heading_open":

                level = int(token.tag[1])

                continue

            if token.type == "inline":

                content = token.content.strip()

                if not content:
                    continue

                block_type = "text"

                heading_level = None

                if token.map:

                    previous_type = tokens[tokens.index(token) - 1].type

                    if previous_type == "heading_open":

                        block_type = "heading"
                        heading_level = level
                        current_heading = content

                block = ContentBlock(
                    block_id=str(uuid.uuid4()),
                    content=content,
                    content_type=block_type,
                    heading_level=heading_level,
                    parent_section=current_heading
                )

                blocks.append(block)

        return StructuredDocument(
            doc_id=raw_document.doc_id,
            source_path=raw_document.source_path,
            blocks=blocks
        )