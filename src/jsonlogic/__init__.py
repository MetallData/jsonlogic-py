from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from types import NoneType
import json
from .operations import Operation, jl_operations
from .errors import JsonLogicArgumentError
from .classes import Entity

PyJsonType = int | float | bool | str | list | dict


class Operand(Entity):
    """An abstract base class representing an JSONLogic operand"""

    def __new__(cls, *_, **__):
        for dunder, op in jl_operations.items():
            setattr(cls, dunder, lambda self, *x, o=op: Expression(o, self, *x))
        return super().__new__(cls)

    def to_dict(self) -> dict[str, Any]:
        """represents the object as as dictionary"""
        raise NotImplementedError()

    def to_json(self) -> str:
        """represents the object as JSON"""
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()


class Variable(Operand):
    """A JSONLogic variable"""

    def __init__(self, var: str):
        super().__init__()
        self.var = var

    def to_dict(self):
        return {"var": self.var}


class Expression(Operand):
    """A JSONLogic expression"""

    def __init__(self, op: Operation, o1: Variable | Expression, *on: Variable | Expression | PyJsonType):
        super().__init__()
        # if op is None then this expression is just a native Selector held in o1.
        self.op = op
        self.o1 = o1
        if op.arity is not None and len(on) != op.arity - 1:
            raise JsonLogicArgumentError(
                f"incorrect number of arguments for {op}: wanted {op.arity}, got {len(on) + 1}"
            )
        self.on = on

    def to_dict(self):
        return {str(self.op): [self.o1.to_dict()] + list(x.to_dict() if isinstance(x, Operand) else x for x in self.on)}


# class Type(ABC):
#     """The abstract base class for all JSONLogic Types"""

# def __init__(self, value):
#     _value = value


# class Number(Type, float):
#     """Type representing a JSONLogic number"""


# class String(Type, str):
#     """Type representing a JSONLogic string"""


# class Object(Type, dict):
#     """Type representing a JSONLogic object (map)"""


# class Bool(Type):
#     """Type representing a JSONLogic boolean"""

#     def __init__(self, value):
#         self.


# class Array(Type, list):
#     """Type representing a JSONLogic array (list)"""


# class Null(Type, NoneType):
#     """Type representing a JSONLogic null"""


# class _Any(Type, Any):
#     """Type representing any JSONLogic type"""
