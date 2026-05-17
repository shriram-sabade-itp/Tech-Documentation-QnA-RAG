class EmbeddingCache:

    def __init__(self):

        self.cache = {}

    def exists(self, checksum):

        return checksum in self.cache

    def get(self, checksum):

        return self.cache.get(checksum)

    def set(self, checksum, embedding):

        self.cache[checksum] = embedding