import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    COHERE_API_KEY = os.getenv(
        "COHERE_API_KEY"
    )

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "./chroma_storage"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    TOP_K_SEMANTIC = int(
        os.getenv(
            "TOP_K_SEMANTIC",
            20
        )
    )

    TOP_K_BM25 = int(
        os.getenv(
            "TOP_K_BM25",
            20
        )
    )

    TOP_K_RERANK = int(
        os.getenv(
            "TOP_K_RERANK",
            10
        )
    )

    MAX_CONTEXT_TOKENS = int(
        os.getenv(
            "MAX_CONTEXT_TOKENS",
            3000
        )
    )


settings = Settings()