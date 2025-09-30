from tools.registry import ToolRegistry
from tools.weather import WeatherTool

registry = ToolRegistry()
registry.register(WeatherTool())

schemas = registry.openai_schemas()
print(schemas)  # OpenAI schema format

# Simulate an LLM tool call
result = registry.execute("get_weather", {"latitude": 51.5074, "longitude": -0.1278})  # London
print(result)
