import requests
from pydantic import BaseModel, Field
from .base import Tool
from typing import Any

class WeatherParams(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class WeatherTool(Tool):
    name = "get_weather"
    description = "Get current temperature and wind speed for given coordinates."
    parameters = WeatherParams

    def run(self, params: WeatherParams) -> dict[str, Any]:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={params.latitude}&longitude={params.longitude}"
            "&current_weather=true"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            return {"error": str(e)}
        data = response.json()

        current = data.get("current_weather", {})
        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "unit": "°C",
        }