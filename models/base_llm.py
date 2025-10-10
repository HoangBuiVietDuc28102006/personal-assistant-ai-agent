import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class LLMResponse(BaseModel):
    output_text: str = Field(..., description="Final textual response from the model.")
    raw_response: Any = Field(..., description="Full raw API response for debugging or logging.")
    tool_calls: Optional[list[dict[str, Any]]] = Field(
        default=None,
        description="List of tool call objects (if any were requested by the model)."
    )

class BaseLLM(ABC):
    def __init__(
            self,
            model_name: str,
            max_tokens: int = 512,
    ):
        if not model_name or not isinstance(model_name, str):
            raise ValueError("model_name must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
        
        self.model_name = model_name
        self.max_tokens = max_tokens
        logger.debug(
            f"{self.__class__.__name__} initialized"
            f"(model={model_name}, max_tokens={max_tokens})"
        )

    @abstractmethod
    def generate(
        self,
        input_list: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None
    ) -> LLMResponse:
        raise NotImplementedError
    
'''
LLMResponse(
    output_text="It’s currently 15°C in London with a windspeed of about 5 km/h.",
    raw_response={
        "id": "resp_abc123",
        "model": "gpt-4o-mini",
        "output": [
            {
                "type": "function_call",
                "name": "get_weather",
                "arguments": "{\"latitude\": 51.5074, \"longitude\": -0.1278}",
                "call_id": "call_001"
            }
        ]
    },
    tool_calls=[
        {
            "name": "get_weather",
            "arguments": "{\"latitude\": 51.5074, \"longitude\": -0.1278}",
            "call_id": "call_001"
        }
    ]
)
'''