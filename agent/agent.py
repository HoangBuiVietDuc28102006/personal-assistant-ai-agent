from models.openai_llm import OpenAILLM
import logging
from prompts.prompt_manager import PromptManager
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from tools.tool_registry import tool_registry
from config.config import Config
import json

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self):
        self.llm = OpenAILLM()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.prompt_manager = PromptManager(
            short_term_memory = self.short_term_memory,
            long_term_memory = self.long_term_memory
        )
        self.tools = tool_registry
        self.tool_schemas = self.tools.schemas()

        logger.debug("Agent initialized with tools: %s", list(self.tools.all().keys()))

    def chat(self, user_input: str):
        logger.info("User input: %s", user_input)

        try:
            # Build a prompt
            input_list = self.prompt_manager.build_prompt(user_input)
            logger.debug("Prompt built: %s", input_list)

            # First response
            response = self.llm.generate(input_list, self.tool_schemas)
            logger.debug("LLM raw response: %s", response.raw_response)

            # Add response to prompt temporarilly
            input_list += response.raw_response.output
            logger.debug("Input list: %s", input_list)

            has_tool_call = False

            logger.debug("Tool calls: %s", response.tool_calls)
            '''
            [
              {
                "name": "get_weather",
                "arguments": {
                  "latitude": 21.0285,
                  "longitude": 105.8542
                },
                "call_id": "call_GZr9awQhrqbdbaiYnX3DItgg"
              }
            ]
            '''

            # Look for tool calls
            if response.tool_calls:
                has_tool_call = True
                for item in response.tool_calls:
                    tool_name = item.get("name")
                    arguments = item.get("arguments")
                    call_id = item.get("call_id")

                    tool = self.tools.get(tool_name)
                    if not tool:
                        logger.warning("⚠️ Tool '%s' not found", tool_name)
                        continue

                    try:
                        logger.info("🤖 Calling tool: %s with args: %s", tool_name, arguments)
                        params = tool.parameters.model_validate_json(arguments)
                        result = tool.run(params)
                        logger.debug("🛠 Tool '%s' result: %s", tool_name, result)
                    except Exception as e:
                        result = {"error": str(e)}
                        logger.error("❌ Tool execution failed: %s", e)

                    # Append tool output to conversation for follow-up LLM call
                    input_list.append({
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": json.dumps(result),
                    })
                    logger.debug("📤 Added tool call output: %s", input_list)

            # === Step 4. Re-query model if a tool was called ===
            if has_tool_call:
                final_response = self.llm.generate(input_list, self.tool_schemas)
                answer = final_response.output_text
                logger.info("✅ Final answer after tool call: %s", answer)
            else:
                answer = response.output_text
                logger.info("✅ Final answer: %s", answer)

            # === Step 5. Save to memory ===
            self.prompt_manager.save_turn(user_input, answer)
            logger.debug("🧠 Conversation turn saved successfully")

            return answer

        except Exception as e:
            logger.exception("🔥 Unhandled error in chat()")
            return "⚠️ Sorry, something went wrong while processing your message."