import logging
from openai import OpenAI
from config.config import Config
from typing import Any
from .base_llm import BaseLLM, LLMResponse

logger = logging.getLogger(__name__)

class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str = Config.MODEL_NAME, max_tokens: int = Config.MAX_TOKENS):
        super().__init__(model_name, max_tokens)
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        logger.debug("OpenAI initialized with model: %s", self.model_name)

    def generate(self, input_list: list, tools: list | None = None):
        logger.info("Generating response using OpenAI: %s", self.model_name)

        try:
            response = self.client.responses.create(
                model=self.model_name,
                tools=tools if tools else None,
                input=input_list,
                max_output_tokens=self.max_tokens,
            )

            text_output = response.output_text

            tool_calls = []
            
            for item in getattr(response, "output", []):
                if getattr(item, "type", None) == "function_call":
                    tool_calls.append({
                        "name": item.name,
                        "arguments": item.arguments,
                        "call_id": item.call_id
                    })
            
            logger.debug("OpenAI response received successfully")
            return LLMResponse(
                output_text=text_output,
                raw_response=response,
                tool_calls=tool_calls or None
            )
        except Exception as e:
            logger.exception("OpenAI generation failed: %s", e)
            raise RuntimeError("Failed to generate OpenAI response") from e