from enum import Enum


class CommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class InteractionRequestType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class InteractionResponseType(Enum):
    PONG = 1
    MESSAGE = 4
    DEFERRED_MESSAGE = 5
    DEFERRED_MESSAGE_UPDATE = 6
    UPDATE_MESSAGE = 7
    AUTOCOMPLETE_RESULT = 8
    MODAL = 9
