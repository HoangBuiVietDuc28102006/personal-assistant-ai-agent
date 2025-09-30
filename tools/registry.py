from tools.base import Tool
from typing import Any, Type

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Type[Tool]):
        self.tools[tool.name] = tool()

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)
    
    def schemas(self) -> list[dict[str, Any]]:
        return [tool.schema() for tool in self.tools.values()]
    
    def execute(self, name: str, args: dict) -> dict[str, Any]:
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found.")
        
        # Validate arguments with the tool’s Pydantic model
        params = tool.parameters.model_validate(args)

        # Run tool and return result
        return tool.run(params)
    
    def all(self) -> dict[str, Tool]:
        """Return all registered tools."""
        return self.tools
    
