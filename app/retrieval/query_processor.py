class QueryProcessor:

    def process(self, query: str):

        """
        Normalize query.
        """

        query = query.strip().lower()

        return query