from google import genai

from app.core.config import settings


class GeminiClient:

    def __init__(self):

        if not settings.GEMINI_API_KEY:

            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = (
            "gemini-2.5-flash-lite"
        )

    def generate(self,
                 system_prompt,
                 user_prompt):

        full_prompt = f"""
{system_prompt}

{user_prompt}
"""

        response = (
            self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
        )

        return response.text