from config.config import Config

class ShortTermMemory:
    def __init__(self, max_turns: int = Config.MAX_MEMORY_TURNS):
        self.max_turns = max_turns
        self.messages = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]

    def get(self):
        return self.messages
    
    def clear(self):
        self.messages = []