class Deduplicator:

    def deduplicate(self, chunks):

        unique = {}

        for chunk in chunks:

            content = chunk["content"]

            if content not in unique:

                unique[content] = chunk

        return list(unique.values())