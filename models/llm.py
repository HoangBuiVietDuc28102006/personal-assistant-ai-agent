from openai import OpenAI
from config.config import Config

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME

    def generate(self, input_list: list, tools: list | None = None):
        response = self.client.responses.create(
            model=self.model,
            tools=tools if tools else None,
            input=input_list,
            max_output_tokens=Config.MAX_TOKENS,
        )
        return response