"""
Tool module.
A tool is a pydantic object that embodies an specific feature that can be executed by the agent. It's structure defines the signature of the function that will be implemented on the `run` method, which will contain the core logic of the feature, it automatically handles the schema definition that is needed by the agent to infer which function to call based on user's natural language input.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Dict, Generic, Literal, TypeVar

from pydantic import BaseModel
from typing_extensions import Required, TypeAlias, TypedDict

from .utils import robust, setup_logging

FunctionParameters: TypeAlias = Dict[str, object]
logger = setup_logging(__name__)

T = TypeVar("T")


class FunctionDefinition(TypedDict, total=False):
    """
    Represents the definition of a function.

    Attributes:
        name (str): The name of the function.
        type (Literal["object"]): The type of the function.
        description (str): The description of the function.
        parameters (FunctionParameters): The parameters of the function.
        required (list[str]): The list of required parameters.
    """

    name: Required[str]
    type: Literal["object"]
    description: Required[str]
    parameters: Required[FunctionParameters]
    required: list[str]


class ToolDefinition(TypedDict, total=False):
    """
    Represents the definition of a tool.

    Attributes:
        type (Literal["function"]): The type of the tool.
        function (FunctionDefinition): The definition of the function.
    """

    type: Required[Literal["function"]]
    function: Required[FunctionDefinition]


class Model(BaseModel):
    """
    This class represents a model used in the application.
    """

    model_config = {"extra": "allow", "arbitrary_types_allowed": True}

    @classmethod
    @lru_cache
    def definition(cls) -> ToolDefinition:
        _schema = cls.model_json_schema()
        assert isinstance(
            cls.__doc__, str
        ), "All models must have a docstring explaining its purpose"
        return {
            "type": "function",
            "function": {
                "name": cls.__name__,
                "description": cls.__doc__,
                "parameters": _schema.get("properties", {}),
                "required": _schema.get("required", []),
            },
        }


class ToolOutput(Model, Generic[T]):
    """
    Represents a response from a tool.

    Attributes:
        content (Any): The content of the response.
        [TODO] Implement output parser class to handle the output `content` of the tools.
        role (str): The role of the response.
    """

    content: T
    role: str


class Tool(Model, ABC):
    """
    Represents a tool used in the application.

    This class provides a base implementation for defining tools.
    Subclasses should override the `run` method to provide the specific
    functionality of the tool.

    Attributes:
        None

    Methods:
        run: Executes the tool and returns the result. [TODO] Add the output parser here.
        __call__: Executes the tool and returns the result as a ToolOutput object.

    """

    @abstractmethod
    async def run(self) -> Any:
        """
        This method is responsible for executing the tool.

        Returns:
            ToolResponse: The response from the tool execution.
        """
        raise NotImplementedError

    @robust
    async def __call__(self) -> ToolOutput[Any]:
        """
        This method is intended to be called by the agent.
        It execute the underlying logic of the tool and returns and object with the result as the `content` attribute and the name of the tool as the `role` attribute in order to be compatible with the `message` format used by the agent and easily distinguishable from other messages to be consumed from the client application. It has a `robust` decorator that catches any exception, handles logging and retries the execution of the tool if it fails on an exponential backoff fashion.
        """
        response = await self.run()
        logger.info("Tool %s executed successfully", response)
        return ToolOutput(content=response, role=self.__class__.__name__.lower())
