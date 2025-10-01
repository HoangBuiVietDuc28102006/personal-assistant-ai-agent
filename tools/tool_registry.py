from .registry import ToolRegistry
from .weather import WeatherTool
from .calculator import CalculatorTool
from .search import SearchTool

tool_registry  = ToolRegistry()
tool_registry.register(WeatherTool)
tool_registry.register(CalculatorTool)
tool_registry.register(SearchTool)