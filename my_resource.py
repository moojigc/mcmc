from re import S
from typing import List, Literal
from flask_restful import Resource, reqparse


class Argument:
    def __init__(self, name: str, type=str, is_required=False) -> None:
        self.name = name
        self.type = type
        self.is_required = is_required


class MyResource(Resource):
    def __init__(self, args: List[Argument]) -> None:
        super().__init__()
        self._args = args
        self.request_args = reqparse.RequestParser()
        for arg in self._args:
            help = f"{arg.name} is required" if arg.is_required else None
            self.request_args.add_argument(
                name=arg.name,
                type=arg.type,
                help=help,
                required=arg.is_required
            )
