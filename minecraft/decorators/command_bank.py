from dataclasses import dataclass
import inspect
import logging
from typing import Callable


@dataclass
class Command:
    func: Callable
    parameters: dict[str, inspect.Parameter]


    def call(self, *args, **kwargs):
        """Call the function and remove unnecessary args"""
        logging.debug(kwargs)
        keyword_args = {k:v for k,v in kwargs.items() if k in self.parameters}

        logging.debug(f"Calling {self.func.__name__} with args: {args} and kwargs: {keyword_args}")

        return self.func(*args, **keyword_args)

class CommandBank:
    def __init__(self) -> None:
        self.holder_cls = None
        self.commands: dict[str, Command] = {}

    def execute(self, command: str, *args, **kwargs):
        if command not in self.commands:
            raise ValueError(f"Command {command} not found!")
        logging.debug(f"Executing command: {command} with kwargs: {kwargs}")

        if self.holder_cls:
            return self.commands.get(command).call(self.holder_cls, *args, **kwargs)
        return self.commands.get(command).call(*args, **kwargs)

    def command_cls(self, holder_cls):
        self.holder_cls = holder_cls
        return holder_cls

    def command_handler(self):
        def wrapper(func: Callable):
            logging.debug("Registering command %s", func.__name__)
            self.commands[func.__name__] = Command(func, inspect.signature(func).parameters)
            return func
        return wrapper


if __name__ == "__main__":

    logging.getLogger().setLevel(logging.DEBUG)

    command_bank = CommandBank()

    @command_bank.command_cls()
    class Test:
        @command_bank.command_handler()
        def send_message(self, message: str, /, name:str=None):
            logging.debug(f"Sending message: {message} from {name or 'Anonymous'}")
    
    command_bank.execute("send_message", "Hello world!", name="Bob")
