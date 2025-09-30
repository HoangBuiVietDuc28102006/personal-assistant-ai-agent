from openai import OpenAI
from config.config import Config
import os

class Embedder:
    def __init__(self):
        self.model = Config.EMBEDDING_MODEL
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def embed(self, text: str) -> list:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding