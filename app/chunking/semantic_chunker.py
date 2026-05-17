from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


class SemanticChunker:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def split_sentences(self, text):

        return text.split(".")

    def semantic_split(self,
                       text,
                       similarity_threshold=0.65):

        sentences = self.split_sentences(text)

        if len(sentences) <= 1:
            return [text]

        embeddings = self.model.encode(sentences)

        chunks = []

        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):

            similarity = cosine_similarity(
                [embeddings[i - 1]],
                [embeddings[i]]
            )[0][0]

            if similarity < similarity_threshold:

                chunks.append(
                    ". ".join(current_chunk)
                )

                current_chunk = [sentences[i]]

            else:

                current_chunk.append(sentences[i])

        if current_chunk:
            chunks.append(". ".join(current_chunk))

        return chunks