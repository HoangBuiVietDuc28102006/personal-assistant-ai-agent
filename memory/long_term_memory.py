from config.config import Config
from models.embedder import Embedder
import psycopg2


class LongTermMemory:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=Config.PG_DBNAME,
            user=Config.PG_USER,
            password=Config.PG_PASSWORD,
            host=Config.PG_HOST,
            port=Config.PG_PORT
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

        self.embedder = Embedder()

    def add(self, role: str, content: str):
        embedding = self.embedder.embed(content)
        self.cur.execute(
            "INSERT INTO user_memories (role, content, embedding) VALUES (%s, %s, %s)",
            (role, content, embedding)
        )

    def search(self, query: str, top_k: int = 2):
        embedding = self.embedder.embed(query)
        self.cur.execute(
            "SELECT role, content FROM user_memories ORDER BY embedding <-> %s::vector LIMIT %s;",
            (embedding, top_k)
        )
        return self.cur.fetchall()