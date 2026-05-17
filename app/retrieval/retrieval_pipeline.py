from app.retrieval.query_processor import (
    QueryProcessor
)

from app.retrieval.semantic_retriever import (
    SemanticRetriever
)

from app.retrieval.bm25_retriever import (
    BM25Retriever
)

from app.retrieval.rrf_fusion import (
    RRFFusion
)

from app.retrieval.parent_retriever import (
    ParentRetriever
)

from app.retrieval.deduplicator import (
    Deduplicator
)

from app.retrieval.context_builder import (
    ContextBuilder
)


class RetrievalPipeline:

    def __init__(self,
                 chroma_collection,
                 bm25_indexer,
                 reranker,
                 all_chunks):

        self.query_processor = (
            QueryProcessor()
        )

        self.semantic_retriever = (
            SemanticRetriever(
                chroma_collection
            )
        )

        self.bm25_retriever = (
            BM25Retriever(
                bm25_indexer
            )
        )

        self.rrf = RRFFusion()

        self.parent_retriever = (
            ParentRetriever()
        )

        self.deduplicator = (
            Deduplicator()
        )

        self.reranker = reranker

        self.context_builder = (
            ContextBuilder()
        )

        self.all_chunks = all_chunks

    def retrieve(self, query):

        # Step 1
        processed_query = (
            self.query_processor.process(
                query
            )
        )

        # Step 2
        semantic_results = (
            self.semantic_retriever.retrieve(
                processed_query
            )
        )

        # Step 3
        bm25_results = (
            self.bm25_retriever.retrieve(
                processed_query
            )
        )

        # Step 4
        fused = self.rrf.fuse(
            semantic_results,
            bm25_results
        )

        # Step 5
        expanded = (
            self.parent_retriever.expand(
                fused,
                self.all_chunks
            )
        )

        # Step 6
        deduplicated = (
            self.deduplicator.deduplicate(
                expanded
            )
        )

        # Step 7
        documents = [
            item["content"]
            for item in deduplicated
        ]

        reranked = self.reranker.rerank(
            query=processed_query,
            documents=documents
        )

        # Step 8
        context = (
            self.context_builder.build(
                reranked
            )
        )

        return {
            "context": context,
            "retrieved_chunks": deduplicated
        }