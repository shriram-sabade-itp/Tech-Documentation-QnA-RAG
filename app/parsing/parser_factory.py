from pathlib import Path

from app.parsing.text_parser import TextParser
from app.parsing.markdown_parser import MarkdownParser


class ParserFactory:

    @staticmethod
    def get_parser(file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".txt":
            return TextParser()

        if extension == ".md":
            return MarkdownParser()

        raise ValueError(f"No parser found for: {extension}")