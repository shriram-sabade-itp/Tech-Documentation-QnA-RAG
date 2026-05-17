from pathlib import Path
from datetime import datetime
import uuid

from app.core.utils import generate_checksum
from app.ingestion.models import RawDocument


class DocumentLoader:

    SUPPORTED_EXTENSIONS = [
        ".txt",
        ".md"
    ]

    def load_document(
            self,
            file_path: str
    ) -> RawDocument:

        path = Path(file_path)

        # -----------------------------------
        # FILE NOT FOUND
        # -----------------------------------

        if not path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # -----------------------------------
        # UNSUPPORTED FILE
        # -----------------------------------

        if (
            path.suffix.lower()
            not in self.SUPPORTED_EXTENSIONS
        ):

            supported = ", ".join(
                self.SUPPORTED_EXTENSIONS
            )

            raise ValueError(
                f"Unsupported file type: "
                f"{path.suffix} | "
                f"Supported: {supported}"
            )

        # -----------------------------------
        # GENERATE CHECKSUM
        # -----------------------------------

        checksum = generate_checksum(
            file_path
        )

        # -----------------------------------
        # LOAD CONTENT
        # -----------------------------------

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        # -----------------------------------
        # RETURN DOCUMENT
        # -----------------------------------

        return RawDocument(

            doc_id=str(uuid.uuid4()),

            file_name=path.name,

            source_path=str(path),

            file_size=path.stat().st_size,

            checksum=checksum,

            version="1.0",

            content=content,

            created_at=datetime.utcnow()
        )