from models.llm import LLM
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from tools.tool_registry import tool_registry
import json

class Agent:
    def __init__(self):
        self.llm = LLM()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.tools = tool_registry

    def chat(self, user_input: str):
        self.short_term_memory.add("user", user_input)

        retrieved_memories = self.long_term_memory.search(
            user_input,
        )
        memory_context = "\n".join([f"{r[0]}: {r[1]}" for r in retrieved_memories])

        input_list  = [{"role": "system", "content": "You are a helpful assistant."}]

        if memory_context.strip():
            input_list.append({
                "role": "system",
                "content": f"Relevant past memories:\n{memory_context}"
            })
        input_list.extend(self.short_term_memory.get())
        input_list.append({"role": "user", "content": user_input})

        response = self.llm.client.responses.create(
            model=self.llm.model,
            tools=self.tools.schemas(),
            input=input_list,
        )

        input_list += response.output

        has_tool_call = False

        for item in response.output:
            if item.type == "function_call":
                has_tool_call = True
                tool = self.tools.get(item.name)
                if not tool:
                    continue

                try:
                    params = tool.parameters.model_validate_json(item.arguments)
                    result = tool.run(params)
                except Exception as e:
                    result = {"error": str(e)}

                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                })

        if has_tool_call:
            final_response = self.llm.client.responses.create(
                model=self.llm.model,
                input=input_list,
                tools=self.tools.schemas(),
            )
            answer = final_response.output_text
        else:
            answer = response.output_text

        self.short_term_memory.add("assistant", answer)

        return answer