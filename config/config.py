import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError(
            "❌ OPENAI_API_KEY is not set. Please add it to your .env file or environment variables."
        )
    
    MODEL_NAME = 'gpt-4o-mini'
    MAX_MEMORY_TURNS = 5
    MAX_TOKENS = 200

    PG_DBNAME = os.getenv('PG_DBNAME')
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')

    EMBEDDING_MODEL = 'text-embedding-3-small'

    DEBUG = True