import os


class CitationFormatter:

    def format(self,
               response_text,
               retrieved_chunks):

        # --------------------------------
        # DO NOT SHOW SOURCES
        # for missing-context response
        # --------------------------------

        fallback_response = (
            "The requested information "
            "is not available in the "
            "retrieved documentation."
        )

        if response_text.strip() == fallback_response:
            return response_text

        citations = []

        seen = set()

        for chunk in retrieved_chunks:

            metadata = chunk.get(
                "metadata",
                {}
            )

            source_path = metadata.get(
                "source_path",
                "Unknown File"
            )

            filename = os.path.basename(
                source_path
            )

            preview = (
                chunk.get("content", "")[:120]
                .replace("\n", " ")
                .strip()
            )

            citation_key = (
                filename,
                preview
            )

            if citation_key in seen:
                continue

            seen.add(citation_key)

            citations.append({
                "filename": filename,
                "preview": preview
            })

        # --------------------------------
        # LIMIT TO FIRST 5 CITATIONS
        # --------------------------------

        max_citations = 5

        displayed = citations[:max_citations]

        remaining = (
            len(citations) - max_citations
        )

        formatted_citations = []

        for citation in displayed:

            formatted_citations.append(
                f'• {citation["filename"]}\n'
                f'  → "{citation["preview"]}..."'
            )

        # --------------------------------
        # SHOW REMAINING COUNT
        # --------------------------------

        if remaining > 0:

            formatted_citations.append(
                f"\n• and other {remaining} citations"
            )

        # --------------------------------
        # APPEND SOURCES
        # --------------------------------

        if formatted_citations:

            response_text += (
                "\n\n---\n"
                "\n## Sources\n\n"
                + "\n\n".join(formatted_citations)
            )

        return response_text