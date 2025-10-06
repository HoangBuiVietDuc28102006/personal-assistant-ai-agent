import logging
from openai import OpenAI
from config.config import Config

logger = logging.getLogger(__name__)

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME
        logger.debug("LLM initialized with model: %s", self.model)

    def generate(self, input_list: list, tools: list | None = None):
        logger.info("🚀 Generating response using model: %s", self.model)

        try:
            response = self.client.responses.create(
                model=self.model,
                tools=tools if tools else None,
                input=input_list,
                max_output_tokens=Config.MAX_TOKENS,
            )
            logger.debug("✅ LLM response received successfully")
            return response
        except Exception as e:
            logger.exception("❌ LLM generation failed: %s", e)
            raise RuntimeError("Failed to generate LLM response") from e