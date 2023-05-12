import sys
from datetime import date, datetime
import logging
from threading import Thread
from urllib.request import Request
from env import DISCORD_SERVER_ID, MOOJCRAFT_APP_ID, MOOJCRAFT_PUBLIC_KEY
from interactions.constants import InteractionRequestType, InteractionResponseType
from interactions.my_utils import initDataclass
from interactions.respond import respond_to_interaction
from utils.my_resource import MyResource, Argument
from flask_restful import request, abort
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import commands
from minecraft.docker_wrapper import DockerExecError
from interactions.Interaction import Interaction
from flask import Flask

automator = commands.create_automator()


class InteractionWebhook(MyResource):
    def post(self):
        try:
            self.verify_signature(req=request)
        except BadSignatureError:
            return {'message': 'invalid request signature'}, 401

        req = request.json
        interaction = initDataclass(Interaction, req)
        # check server is Moojcraft server!
        self.verify_server_is_allowed(interaction)

        if interaction.type == InteractionRequestType.PING:
            return respond_to_interaction(type=InteractionResponseType.PONG)
        else:
            try:
                return self.__handle(interaction)
            except DockerExecError as e:
                return respond_to_interaction(e)
            except Exception as e:
                logging.error(e)
                return respond_to_interaction(repr(e))

    def send_docker_server_command(self, interaction: Interaction):
        logging.info(interaction.data.options[0].value)
        msg = ""
        if interaction.data.options[0].value == "on":
            try:
                msg = automator.on()
            except Exception as e:
                msg = str(e)
            return interaction.make_follow_up_response(msg)
        try:
            msg = automator.docker_wrapper.shutdown(delay=10)
            return interaction.make_follow_up_response(msg)
        except Exception as e:
            return interaction.make_follow_up_response(str(e))

    def verify_server_is_allowed(self, interaction: Interaction) -> None:
        if interaction.type != InteractionRequestType.PING and interaction.guild_id != DISCORD_SERVER_ID:
            abort(403, message="Unauthorized server")

    def get_command_is_allowed(self, interaction: Interaction) -> bool:
        logging.info("Checking command permissions???")
        hour = datetime.now().hour
        is_night_time = 0 < hour < 7
        logging.debug(f'{is_night_time=}')
        logging.debug(f"{interaction.is_restricted_command=}")
        logging.debug(f'{interaction.is_user_moojig=}')
        if not is_night_time and interaction.is_restricted_command:
            return interaction.is_user_moojig
        else:
            return True

    def verify_signature(self, req: Request):
        """verify the headers from discord. Raises a BadSignatureError"""
        verify_key = VerifyKey(bytes.fromhex(MOOJCRAFT_PUBLIC_KEY))

        signature = req.headers["X-Signature-Ed25519"]
        timestamp = req.headers["X-Signature-Timestamp"]
        body = req.data.decode("utf-8")
        verify_key.verify(f'{timestamp}{body}'.encode(),
                          bytes.fromhex(signature))

    def __handle(self, interaction: Interaction):
        cmd_name = interaction.data.name
        print(interaction.data)
        if not self.get_command_is_allowed(interaction):
            return respond_to_interaction(f"ayo *{interaction.get_user.username}* not allowed to do that until after **midnight**")
        if cmd_name == 'ping':
            res_msg = automator.ping()
        elif cmd_name == "server":
            thread = Thread(target=lambda: self.send_docker_server_command(
                interaction))
            try:
                thread.start()
            except Exception as e:
                return respond_to_interaction(str(e))
            return respond_to_interaction("Sending shutdown command...", type=InteractionResponseType.DEFERRED_MESSAGE)
        elif cmd_name == "players":
            res_msg = automator.players()
        else:
            option = interaction.data.options[0]
            print(f"{interaction.data.options=}")
            name = interaction.member.user.username
            res_msg = automator.chat(option.value, player_name=name)
        return respond_to_interaction(res_msg)
