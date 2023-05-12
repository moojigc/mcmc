from ast import Lambda
from dataclasses import dataclass, field
from typing import Any, Literal

from interactions.constants import InteractionResponseType


def respond_to_interaction(content: str = None, type: InteractionResponseType = InteractionResponseType.MESSAGE, deferred_action: Lambda = None):
    return {
        "type": type.value,
        "data": {
            "tts": False,
            "content": str(content)
        }
    }
