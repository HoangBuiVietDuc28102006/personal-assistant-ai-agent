from abc import ABC, abstractmethod
from typing import Type, Any
from pydantic import BaseModel

class Tool(ABC):
    name: str
    description: str
    parameters: Type[BaseModel]

    def __init_subclass__(cls):
        if not hasattr(cls, "name") or not cls.name:
            raise TypeError(f"{cls.__name__} must define a name")
        if not hasattr(cls, "description") or not cls.description:
            raise TypeError(f"{cls.__name__} must define a description")
        if not hasattr(cls, "parameters") or not issubclass(cls.parameters, BaseModel):
            raise TypeError(f"{cls.__name__} must define a Pydantic parameters model")

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "type": "function",
            "name": cls.name,
            "description": cls.description,
            "parameters": cls.parameters.model_json_schema(),
        }
    
    @abstractmethod
    def run(self, params: BaseModel) -> Any:
        pass