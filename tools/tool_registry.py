from .registry import ToolRegistry
from .weather import WeatherTool

tool_registry  = ToolRegistry()
tool_registry.register(WeatherTool)