from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Any, Dict

# ----------------------------
# Base Tool
# ----------------------------
class Tool:
    name: str
    description: str
    parameters: BaseModel

    @classmethod
    def schema(cls) -> Dict[str, Any]:
        """Return OpenAI Responses API tool schema"""
        return {
            "type": "function",
            "name": cls.name,
            "description": cls.description,
            "parameters": cls.parameters.model_json_schema(),
        }

    def run(self, **kwargs) -> Any:
        raise NotImplementedError


# ----------------------------
# Weather Tool Implementation
# ----------------------------
class WeatherParams(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class WeatherTool(Tool):
    name = "get_weather"
    description = "Get current temperature and wind speed for given coordinates."
    parameters = WeatherParams

    def run(self, **kwargs) -> dict:
        params = self.parameters(**kwargs)  # validate input
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={params.latitude}&longitude={params.longitude}"
            f"&current=temperature_2m,wind_speed_10m"
        )
        return response.json().get("current", {})


# ----------------------------
# Setup OpenAI client + tool
# ----------------------------
client = OpenAI()
weather_tool = WeatherTool()
tools = [weather_tool.schema()]

# User input
input_list = [
    {"role": "user", "content": "What's the weather in Sydney? Coordinates are -33.8688, 151.2093"}
]

# Step 1: Ask model with tool definitions
response = client.responses.create(
    model="gpt-4o-mini",
    tools=tools,
    input=input_list,
)

# Save function call outputs for subsequent requests
input_list += response.output

# Step 2: Handle tool calls
for item in response.output:
    if item.type == "function_call" and item.name == weather_tool.name:
        args = json.loads(item.arguments)
        result = weather_tool.run(**args)

        # Provide tool output back to the model
        input_list.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(result),
        })

print("Final input to model:")
for item in input_list:
    if hasattr(item, "model_dump_json"):
        print(item.model_dump_json(indent=2))
    else:
        print(json.dumps(item, indent=2))

# Step 3: Get final model answer
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Respond only with the weather details from the tool output.",
    tools=tools,
    input=input_list,
)

print("\nFinal output JSON:")
print(response.model_dump_json(indent=2))
print("\nAssistant:", response.output_text)
print("-----------------------")
print(json.dumps(weather_tool.schema(), indent=2))
