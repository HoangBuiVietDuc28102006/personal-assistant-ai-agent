from tools.weather import WeatherTool


def test_weather_tool_schema():
    tool = WeatherTool()
    schema = tool.to_openai_schema()

    assert schema["type"] == "function"
    assert schema["function"]["name"] == "get_weather"
    assert "parameters" in schema["function"]
    assert "properties" in schema["function"]["parameters"]
    assert "latitude" in schema["function"]["parameters"]["properties"]
    assert "longitude" in schema["function"]["parameters"]["properties"]
