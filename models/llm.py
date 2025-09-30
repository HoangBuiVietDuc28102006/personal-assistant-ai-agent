from openai import OpenAI
from config.config import Config

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME

    def generate(self, input_list: list):
        with self.client.responses.stream(
            model=self.model,
            input=input_list,
            max_output_tokens=Config.MAX_TOKENS,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
                elif event.type == "response.completed":
                    break
            stream.close()