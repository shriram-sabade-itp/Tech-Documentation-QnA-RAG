from collections import defaultdict


class RRFFusion:

    def fuse(self,
             semantic_results,
             bm25_results,
             k=60):

        scores = defaultdict(float)

        documents = {}

        # Semantic rankings
        for rank, result in enumerate(
                semantic_results):

            doc_key = result["content"]

            scores[doc_key] += (
                1 / (k + rank + 1)
            )

            documents[doc_key] = result

        # BM25 rankings
        for rank, result in enumerate(
                bm25_results):

            doc_key = result["content"]

            scores[doc_key] += (
                1 / (k + rank + 1)
            )

            documents[doc_key] = result

        fused = []

        for doc_key, score in scores.items():

            item = documents[doc_key]

            item["rrf_score"] = score

            fused.append(item)

        fused.sort(
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        return fused