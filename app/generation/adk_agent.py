from app.generation.gemini_client import (
    GeminiClient
)

from app.generation.prompt_builder import (
    PromptBuilder
)

from app.generation.response_validator import (
    ResponseValidator
)


class RAGAgent:

    def __init__(self):

        self.prompt_builder = (
            PromptBuilder()
        )

        self.gemini = GeminiClient()

        self.validator = (
            ResponseValidator()
        )

    def answer(self,
               query,
               context):

        prompts = (
            self.prompt_builder.build(
                query,
                context
            )
        )

        response = self.gemini.generate(
            system_prompt=(
                prompts["system_prompt"]
            ),
            user_prompt=(
                prompts["user_prompt"]
            )
        )

        valid = self.validator.validate(
            response
        )

        if not valid:

            return (
                "Generation failed."
            )

        return response