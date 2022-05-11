from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List


class ValueType(Enum):
    STR = 3
    NUMERIC = 4


@dataclass
class Option:
    name: str
    type: int
    value: Any


@dataclass
class Message:
    id: str
    name: str
    value: Any
    options: field(default_factory=lambda xs: [Option(x) for x in xs])
