from app.core.logger import logger
from app.parsing.parser_factory import ParserFactory


class StructuredExtractor:

    def extract(self, raw_document):

        logger.info("Starting structured extraction")

        parser = ParserFactory.get_parser(
            raw_document.source_path
        )

        structured_document = parser.parse(raw_document)

        logger.info(
            f"Extracted {len(structured_document.blocks)} blocks"
        )

        return structured_document