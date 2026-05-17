from app.generation.system_prompt import (
    SYSTEM_PROMPT
)


class PromptBuilder:

    def build(self,
              query,
              context):

        user_prompt = f"""
            USER QUESTION:
            {query}

            --------------------
            RETRIEVED CONTEXT
            --------------------

            {context}

            --------------------
            ANSWER
            --------------------
        """

        return {
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": user_prompt
        }