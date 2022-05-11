import json
import logging
from typing import Any, List
from my_resource import MyResource, Argument
from flask_restful import request, abort
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from minecraft.automation import DockerExecError, main as send_mc_command
from interactions.Interaction import Interaction


class InteractionWebhook(MyResource):
    def __init__(self) -> None:
        super().__init__(
            []
        )

    def __handle(self, req):
        interaction = Interaction(**req)
        print(interaction)
        cmd_name = interaction.data['name']
        if cmd_name == 'ping':
            msg: str
            msg = send_mc_command("ping")
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg
                }
            }
        elif cmd_name == "server":
            option = interaction.data['options'][0]
            msg = send_mc_command(option['value'])
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg
                }
            }
        elif cmd_name == "players":
            msg = send_mc_command("count")
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg
                }
            }
        else:
            option = interaction.data['options'][0]
            name = interaction.member['user']['username']
            res_msg = send_mc_command(
                "send_message", message=option['value'], source="DISCORD", name=name)
            return {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": res_msg
                }
            }

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
        if req['type'] == 1:
            return {
                "type": 1
            }
        else:
            try:
                return self.__handle(req=request.json)
            except DockerExecError as e:
                return {
                    "type": 4,
                    "data": {
                        "tts": False,
                        "content": e.message
                    }
                }
            except Exception as e:
                raise e
                logging.debug(e)
                return {
                    "type": 4,
                    "data": {
                        "tts": False,
                        "content": repr(e)
                    }
                }
