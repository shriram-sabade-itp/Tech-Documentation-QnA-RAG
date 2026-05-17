# RAG System — Edge Case Matrix

| ID | Module | Edge Case | Input Scenario | Expected Behavior | Status |
|---|---|---|---|---|---|
| EC-001 | Ingestion | No file provided | User presses enter | Show Rich error box: `No files provided` | Handled |
| EC-002 | Ingestion | Empty file list | `[]` passed to ingest | Raise validation error | Handled |
| EC-003 | Ingestion | Invalid file path | Non-existent file | Skip file + log error | Handled |
| EC-004 | Ingestion | Unsupported file type | `.exe`, `.dll`, `.zip` | Skip file + warning/error panel | Handled |
| EC-005 | Ingestion | Mixed valid + invalid files | 2 valid + 1 invalid | Process valid files only | Handled |
| EC-006 | Ingestion | Duplicate document | Same checksum uploaded again | Skip ingestion | Handled |
| EC-007 | Ingestion | Same filename, different content | `notes.txt` modified | Treat as new document | Handled |
| EC-008 | Ingestion | Empty document | Blank `.txt` | Warning: no chunks generated | Handled |
| EC-009 | Ingestion | Special characters | Emojis/symbols/code | No tokenizer crash | Partial |
| EC-010 | Metadata | Missing metadata fields | No headings/pages | Use defaults/None | Handled |
| EC-011 | Metadata | Invalid datetime | Serialization issue | Convert to ISO string | Handled |
| EC-012 | Metadata | Unsupported Chroma metadata types | lists/dicts | Sanitize metadata | Handled |
| EC-013 | Embeddings | Embedding cache hit | Existing checksum | Reuse cached embedding | Handled |
| EC-014 | ChromaDB | Empty collection | Query before ingest | Show "No documents found" | Handled |
| EC-015 | ChromaDB | Duplicate chunk IDs | Same chunk inserted twice | Upsert overwrite | Handled |
| EC-016 | Retrieval | No retrieval matches | Irrelevant query | Return missing-context response | Handled |
| EC-017 | Retrieval | Semantic only hit | BM25 no match | Continue retrieval | Handled |
| EC-018 | Retrieval | BM25 only hit | Semantic weak | Continue retrieval | Handled |
| EC-019 | Retrieval | Duplicate retrievals | Same chunk from BM25 + semantic | Deduplicate | Handled |
| EC-020 | Retrieval | Parent chunk missing | Invalid parent ID | Skip safely | Handled |
| EC-021 | Generation | Empty context | No retrievals | Return fallback message | Handled |
| EC-022 | Generation | Hallucination risk | Weak context | Strict grounding | Handled |
| EC-023 | Generation | Citation spam | Too many citations | Limit to first 7 | Handled |
| EC-024 | Generation | Duplicate citations | Same chunk repeated | Deduplicate citations | Handled |
| EC-025 | Generation | Citation after every sentence | Verbose formatting | Consolidated bottom citations | Handled |
| EC-026 | Query Service | Exit loop | User types exit | Graceful shutdown | Handled |
| EC-027 | Logging | Console spam | Too many logs | Save logs to file only | Handled |
| EC-028 | Logging | Missing logs directory | `logs/` absent | Auto-create folder | Partial |
| EC-029 | CLI UI | Successful ingestion summary | Multiple files | Show filenames + chunk counts | Handled |
| EC-030 | Persistence | Restart query service | Existing DB | Reload indexes correctly | Handled |
| EC-031 | Persistence | Schema mismatch | Old metadata structure | Mapper normalization | Handled |
| EC-032 | Architecture | Dict vs object mismatch | Mixed schema usage | ChunkMapper normalization | Handled |
| EC-033 | Architecture | Missing environment variables | API key absent | Validation failure | Handled |
| EC-034 | Security | Prompt injection inside docs | Malicious retrieved text | Grounded-only generation | Partial |
| EC-035 | Scalability | Huge Chroma collection | Millions of chunks | Requires pagination/sharding | Not Implemented |
| EC-036 | Recovery | Crash during ingestion | Mid-pipeline failure | Checkpoint recovery | Partial |