import cohere

from app.core.config import settings


class CohereReranker:

    def __init__(self):

        if not settings.COHERE_API_KEY:

            raise ValueError(
                "COHERE_API_KEY not found."
            )

        self.client = cohere.Client(
            settings.COHERE_API_KEY
        )

    def rerank(self,
               query,
               documents,
               top_k=10):

        try:

            response = self.client.rerank(
                model="rerank-english-v3.0",

                query=query,

                documents=documents,

                top_n=top_k
            )

            reranked = []

            for result in response.results:

                reranked.append({

                    "content":
                        documents[result.index],

                    "score":
                        result.relevance_score
                })

            return reranked

        except Exception as e:

            return [{
                "content":
                    f"ERROR: {str(e)}",

                "score": 0.0
            }]