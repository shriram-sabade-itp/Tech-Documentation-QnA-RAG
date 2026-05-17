from app.core.logger import logger
from app.generation.adk_agent import (
    RAGAgent
)

from app.generation.citation_formatter import (
    CitationFormatter
)


class GenerationPipeline:

    def __init__(self):

        self.agent = RAGAgent()

        self.citation_formatter = (
            CitationFormatter()
        )

    logger.info("Starting generation")
    
    def generate(self,
                 query,
                 context,
                 retrieved_chunks):
        
        logger.info(
            f"Context length: {len(context)}"
        )

        if (
            context
            == "NO_CONTEXT_AVAILABLE"
        ):

            return (
                "The requested information "
                "is not available in the "
                "retrieved documentation."
            )

        response = self.agent.answer(
            query,
            context
        )

        final_response = (
            self.citation_formatter.format(
                response,
                retrieved_chunks
            )
        )

        logger.info("Generation completed")
        
        return final_response