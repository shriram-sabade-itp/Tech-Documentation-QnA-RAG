import os
from datetime import datetime
from typing import List, Union
from app.core.logger import logger
from app.ingestion.loader import DocumentLoader
from app.ingestion.file_registry import FileRegistry
from app.ingestion.checkpoint_manager import CheckpointManager
from app.ingestion.models import Checkpoint
from app.metadata.metadata_enricher import MetadataEnricher
from app.parsing.structured_extractor import StructuredExtractor
from app.chunking.chunking_pipeline import ChunkingPipeline
from app.embeddings.embedding_service import EmbeddingService
from app.indexing.indexing_pipeline import IndexingPipeline


class IngestionPipeline:

    def __init__(self):

        self.embedding_service = EmbeddingService()
        self.indexing_pipeline = IndexingPipeline()

        self.loader = DocumentLoader()
        self.registry = FileRegistry()
        self.extractor = StructuredExtractor()
        self.chunking_pipeline = ChunkingPipeline()
        self.metadata_enricher = MetadataEnricher()

    def ingest(self, file_path: Union[str, List[str]]):
        try:

            if file_path is None:
                raise ValueError("No file path provided for ingestion.")

            if isinstance(file_path, str):
                file_path = [file_path]

            if len(file_path) == 0:
                raise ValueError("Empty file list provided for ingestion.")

            all_embedded_chunks = []

            logger.info(f"Starting batch ingestion: {len(file_path)} files")

            successful_files = 0

            failed_files = []

            warning_files = []

            successful_file_names = []

            empty_chunk_files = []
            
            for path in file_path:

                # ----------------------------
                # STEP 1: Validate file input
                # ----------------------------
                if not path or not isinstance(path, str):
                    message = (
                        f"[SKIP] Invalid file path skipped: {path}"
                    )

                    logger.warning(message)

                    warning_files.append(message)
                    continue

                if not os.path.exists(path):
                    message = f"[SKIP] File not found: {path}"

                    logger.error(message)

                    failed_files.append(message)
                    continue

                try:
                    logger.info(f"Starting ingestion: {path}")

                    # ----------------------------
                    # STEP 2: Load document
                    # ----------------------------
                    try:

                        raw_document = (
                            self.loader.load_document(path)
                        )

                    except Exception as load_error:

                        message = (
                            f"[UNSUPPORTED] Unsupported or unreadable file: "
                            f"{path}"
                        )

                        logger.error(message)

                        failed_files.append(message)

                        continue

                    if self.registry.is_already_ingested(raw_document.checksum):
                        message = (
                            f"[SKIP] Duplicate document: {path}"
                        )

                        logger.warning(message)
                        warning_files.append(message)
                        continue

                    # ----------------------------
                    # STEP 3: Processing pipeline
                    # ----------------------------
                    try:
                        structured_document = self.extractor.extract(raw_document)
                    except Exception as extract_error:
                        logger.error(
                            f"[EXTRACTION FAILED] {path} | Error: {str(extract_error)}"
                        )
                        failed_files.append(f"[EXTRACTION FAILED] {path}")
                        continue

                    checkpoint = Checkpoint(
                        doc_id=raw_document.doc_id,
                        status="PARSED",
                        last_updated=datetime.utcnow()
                    )

                    CheckpointManager.save_checkpoint(checkpoint)

                    self.registry.register_document(
                        raw_document.checksum,
                        raw_document.doc_id
                    )

                    chunks = self.chunking_pipeline.process(structured_document)

                    enriched_chunks = self.metadata_enricher.enrich(
                        chunks,
                        raw_document
                    )

                    embedded_chunks = self.embedding_service.embed_chunks(
                        enriched_chunks
                    )

                    # --------------------------------
                    # EMPTY CHUNK FILE
                    # --------------------------------

                    if not embedded_chunks:

                        message = (
                            f"[NO CHUNKS] No chunks generated: {path}"
                        )

                        logger.warning(message)

                        warning_files.append(message)

                        empty_chunk_files.append(path)

                        continue

                    # --------------------------------
                    # SUCCESS
                    # --------------------------------

                    all_embedded_chunks.extend(
                        embedded_chunks
                    )

                    successful_files += 1

                    successful_file_names.append(
                        os.path.basename(path)
                    )

                    logger.info(
                        f"[SUCCESS] File: {path} | chunks={len(embedded_chunks)}"
                    )

                except Exception as file_error:
                    # ✅ IMPORTANT: per-file failure isolation
                    logger.error(
                        f"[FAILED FILE] {path} | Error: {str(file_error)}"
                    )
                    continue

            logger.info(
                f"TOTAL INGESTED CHUNKS: {len(all_embedded_chunks)}"
            )

            logger.info(
                f"SUCCESSFUL FILES: {successful_files}"
            )

            logger.info(
                f"FAILED FILES: {len(failed_files)}"
            )

            logger.info(
                f"WARNING FILES: {len(warning_files)}"
            )

            return {
                "embedded_chunks": all_embedded_chunks,

                "successful_files": successful_files,

                "successful_file_names":
                    successful_file_names,

                "empty_chunk_files":
                    empty_chunk_files,

                "failed_files":
                    failed_files,

                "warning_files":
                    warning_files
            }

        except Exception as error:
            logger.error(f"Ingestion batch failed: {str(error)}")
            return []