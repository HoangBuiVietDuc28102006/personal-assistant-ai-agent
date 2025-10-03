from config.config import Config
from models.embedder import Embedder
import psycopg2


class LongTermMemory:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.enabled = True
        try:
            self.conn = psycopg2.connect(
                dbname=Config.PG_DBNAME,
                user=Config.PG_USER,
                password=Config.PG_PASSWORD,
                host=Config.PG_HOST,
                port=Config.PG_PORT
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"[WARN] LongTermMemory disabled (DB error: {e})")
            self.enabled = False

        self.embedder = Embedder()

    def add(self, role: str, content: str):
        if not self.enabled:
            return
        
        try:
            embedding = self.embedder.embed(content)
            self.cur.execute(
                "INSERT INTO user_memories (role, content, embedding) VALUES (%s, %s, %s)",
                (role, content, embedding)
            )
        except Exception as e:
            print(f"[ERROR] Failed to save memory: {e}")

    def search(self, query: str, top_k: int = 2):
        if not self.enabled:
            return []
        
        try:
            embedding = self.embedder.embed(query)
            self.cur.execute(
                "SELECT role, content FROM user_memories ORDER BY embedding <-> %s::vector LIMIT %s;",
                (embedding, top_k)
            )
            return self.cur.fetchall()
        except Exception as e:
            print(f"[ERROR] Memory search failed: {e}")
            return []