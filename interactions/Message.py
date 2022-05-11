from dataclasses import dataclass
from enum import Enum
from typing import Any, List


class ValueType(Enum):
    STR = 3
    NUMERIC = 4


@dataclass
class Options:
    name: str
    type: ValueType.value
    value: Any


@dataclass
class Message:
    id: str
    name: str
    value: Any
    options: List[Options]
