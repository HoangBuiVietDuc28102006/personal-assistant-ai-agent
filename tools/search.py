# tools/search.py
import requests
from pydantic import BaseModel, Field
from .base import Tool
from typing import Any

class SearchParams(BaseModel):
    query: str = Field(..., description="Search query text")

class SearchTool(Tool):
    name = "web_search"
    description = "Search the web for information."
    parameters = SearchParams

    def run(self, params: SearchParams) -> dict[str, Any]:
        url = f"https://api.duckduckgo.com/?q={params.query}&format=json"
        try:
            res = requests.get(url, timeout=10).json()
            results = [r["Text"] for r in res.get("RelatedTopics", []) if "Text" in r]
            return {"results": results[:5]}
        except Exception as e:
            return {"error": str(e)}
