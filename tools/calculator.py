# tools/calculator.py
from pydantic import BaseModel, Field
from .base import Tool
from typing import Any

class CalculatorParams(BaseModel):
    expression: str = Field(..., description="A math expression to evaluate safely")

class CalculatorTool(Tool):
    name = "calculate"
    description = "Evaluate a math expression (e.g., '2 + 2 * 5')."
    parameters = CalculatorParams

    def run(self, params: CalculatorParams) -> dict[str, Any]:
        try:
            result = eval(params.expression, {"__builtins__": {}})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
