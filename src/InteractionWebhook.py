import json
import logging
from typing import Any, List
from my_resource import MyResource, Argument
from flask_restful import request, abort
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from minecraft.automation import DockerExecError, main as send_mc_command


class InteractionWebhook(MyResource):
    def __init__(self) -> None:
        super().__init__(
            []
        )

    def post(self):
        # Your public key can be found on your application in the Developer Portal
        PUBLIC_KEY = 'e19867538e064e1e9a87e295f36aad6db3d9e4e649137428029dee2d9a25a86d'

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        body = request.data.decode("utf-8")

        try:
            verify_key.verify(f'{timestamp}{body}'.encode(),
                              bytes.fromhex(signature))
        except BadSignatureError:
            return 'invalid request signature', 401

        req = request.json
        cmd_name = req['data']['name']
        if cmd_name == 'ping':
            msg: str
            try:
                msg = send_mc_command("ping")
            except DockerExecError as e:
                print(e.message)
                msg = e.message or "Something went wrong! IDK WHAT FAM!"
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg
                }
            }
        elif cmd_name == "server":
            options: List[Any] = req['data']['options']
            option = options[0]['value']
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": option
                }
            }
        else:
            options: List[Any] = req['data']['options']
            msg = options[0]['value']
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg
                }
            }
