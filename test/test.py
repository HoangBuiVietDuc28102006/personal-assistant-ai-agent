# agent.py
from models.llm import LLM
from prompts.prompt_manager import PromptManager
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from tools.tool_registry import tool_registry
from config.config import Config
import json

class Agent:
    def __init__(self):
        self.llm = LLM()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.prompt_manager = PromptManager(
            short_term_memory = self.short_term_memory,
            long_term_memory = self.long_term_memory
        )
        self.tools = tool_registry

    def chat(self, user_input: str):
        # Add user message
        input_list = self.prompt_manager.build_prompt(user_input)

        # First response (may or may not call a tool)
        response = self.llm.client.responses.create(
            model=self.llm.model,
            tools=self.tools.schemas(),
            input=input_list,
        )

        input_list += response.output
        has_tool_call = False

        # 🔎 Look for tool calls
        for item in response.output:
            if item.type == "function_call":
                has_tool_call = True
                tool = self.tools.get(item.name)
                if not tool:
                    if Config.DEBUG:
                        print(f"⚠️ Tool '{item.name}' not found")
                    continue

                try:
                    if Config.DEBUG:
                        print(f"🤖 Decided to call tool: {item.name} with args: {item.arguments}")
                    params = tool.parameters.model_validate_json(item.arguments)
                    result = tool.run(params)
                    if Config.DEBUG:
                        print(f"🛠 Tool result: {result}")
                except Exception as e:
                    result = {"error": str(e)}
                    if Config.DEBUG:
                        print(f"❌ Tool execution failed: {e}")

                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                })

        # If a tool was called, re-ask LLM with results
        if has_tool_call:
            final_response = self.llm.client.responses.create(
                model=self.llm.model,
                input=input_list,
                tools=self.tools.schemas(),
            )
            answer = final_response.output_text
        else:
            answer = response.output_text

        # Save user input and agent output
        self.prompt_manager.save_turn(user_input, answer)

        return answer