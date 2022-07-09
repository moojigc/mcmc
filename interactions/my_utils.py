from dataclasses import fields
from typing import Type, Generic


def initDataclass(Cls, kwargs):
    """Ignore extra keyword arguments in dataclass"""
    names = set([f.name for f in fields(Cls)])
    print(names)
    return Cls(**{
        k: v for k, v in kwargs.items() if k in names
    })
