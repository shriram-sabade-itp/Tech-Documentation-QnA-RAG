class ContextBuilder:

    def build(self,
              reranked_results,
              max_tokens=3000):

        context = []

        token_count = 0

        for result in reranked_results:

            content = result["content"]

            estimated_tokens = len(
                content.split()
            )

            if (
                token_count
                + estimated_tokens
                > max_tokens
            ):

                break

            context.append(content)

            token_count += estimated_tokens

        return "\n\n".join(context)