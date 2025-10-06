import logging
from config.config import Config
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, short_term_memory: ShortTermMemory, long_term_memory: LongTermMemory):
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory
        self.base_system_prompt = "You are a helpful assistant."

    def build_prompt(self, user_input: str) -> list[dict]:
        input_list = [{"role": "system", "content": self.base_system_prompt}]

        retrieved = self.long_term_memory.search(user_input)
        memory_context = "\n".join([f"{r[0]}: {r[1]}" for r in retrieved])

        if memory_context.strip():
            input_list.append({
                "role": "system",
                "content": f"Relevant past memories:\n{memory_context}"
            })

        input_list.extend(self.short_term_memory.get())

        input_list.append({"role": "user", "content": user_input})

        return input_list
    
    def save_turn(self, user_input: str, assistant_reply: str):
        """
        Persist the latest interaction into short and long term memories.
        """
        self.short_term_memory.add("user", user_input)
        self.short_term_memory.add("assistant", assistant_reply)