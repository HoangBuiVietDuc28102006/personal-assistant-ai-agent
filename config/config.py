import os
from dotenv import load_dotenv
import logging

load_dotenv()

class BaseConfig:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_NAME = 'gpt-4o-mini'
    MAX_MEMORY_TURNS = 5
    MAX_TOKENS = 200
    
    EMBEDDING_MODEL = 'text-embedding-3-small'

class DevConfig(BaseConfig):
    DEBUG = True
    PG_DBNAME = os.getenv('PG_DBNAME')
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')

class ProdConfig(BaseConfig):
    DEBUG = False
    PG_DBNAME = os.getenv('PG_DBNAME')
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')

def get_config():
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProdConfig()
    return DevConfig()

Config = get_config()

logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)