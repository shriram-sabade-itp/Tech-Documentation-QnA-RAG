from app.core.config import settings


class EnvValidator:

    @staticmethod
    def validate():

        required_keys = [

            "GEMINI_API_KEY",

            "COHERE_API_KEY"
        ]

        missing = []

        for key in required_keys:

            value = getattr(
                settings,
                key
            )

            if not value:

                missing.append(key)

        if missing:

            raise ValueError(
                "Missing environment variables: "
                + ", ".join(missing)
            )

        print(
            "Environment validation passed."
        )