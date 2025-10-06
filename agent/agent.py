from models.llm import LLM
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
        self.llm = LLM()
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

            # Add response to prompt temporarilly
            input_list += response.output
            logger.debug("LLM raw response: %s", response.output)

            has_tool_call = False

            # Look for tool calls
            for item in response.output:
                if item.type == "function_call":
                    has_tool_call = True
                    tool = self.tools.get(item.name)
                    if not tool:
                        logger.warning("Tool '%s' not found", item.name)
                        continue

                    try:
                        logger.info("Calling tool: %s with args: %s", item.name, item.arguments)
                        params = tool.parameters.model_validate_json(item.arguments)
                        result = tool.run(params)
                        logger.debug("Tool '%s' result: %s", item.name, result)
                    except Exception as e:
                        result = {"error": str(e)}
                        logger.error("Tool execution failed: %s", e)

                    input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result),
                    })
                    logger.debug("Added tool call output: %s", input_list)

            # If a tool was called, re-ask LLM with results
            if has_tool_call:
                final_response = self.llm.generate(input_list, self.tool_schemas)

                answer = final_response.output_text
                logger.info("Final answer after tool call: %s", answer)
            else:
                answer = response.output_text
                logger.info("Final answer: %s", answer)

            # Save user input and agent output
            self.prompt_manager.save_turn(user_input, answer)

            logger.debug("Conversation turn saved successfully")

            return answer
        except Exception as e:
            logger.exception("Unhandled error in chat()")
            return "Sorry, something went wrong while processing your message."