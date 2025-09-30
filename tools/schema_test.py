from jsonschema import Draft7Validator
from tools.weather import WeatherTool

schema = WeatherTool.schema()["function"]["parameters"]
Draft7Validator.check_schema(schema)
print("✅ Schema matches Draft-07 JSON Schema")
