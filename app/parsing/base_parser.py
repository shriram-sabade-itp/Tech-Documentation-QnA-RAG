from abc import ABC, abstractmethod

from app.parsing.models import StructuredDocument


class BaseParser(ABC):

    @abstractmethod
    def parse(self, raw_document) -> StructuredDocument:
        pass