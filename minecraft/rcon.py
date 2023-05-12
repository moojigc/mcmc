import logging
import re
from datetime import datetime
from time import sleep, time
from typing import List

from docker import errors as docker_errors

from .discord import DiscordMessenger
from .docker_wrapper import DockerExecError, DockerAsleepError, DockerWrapper


class Rcon:
    """interact with rcon-cli"""
    def __init__(self, docker_wrapper: DockerWrapper, discord_messenger: DiscordMessenger) -> None:
        self.docker_wrapper = docker_wrapper
        self.discord_messenger = discord_messenger

    def _cmd(self, cmd_str: str) -> str:
        try:
            result = self.docker_wrapper.minecraft_server.exec_run(
                f"rcon-cli {cmd_str}")
            if result.exit_code > 0:
                raise DockerExecError(result.output.decode())
            string_res = result.output.decode()
            if isinstance(string_res, str) and "connect" in string_res:
                raise DockerAsleepError("Server is still starting...")
            return string_res
        except docker_errors.APIError:
            raise DockerAsleepError("MC MC server is asleep.")

    def save(self):
        logging.info("Saving...")
        res = self._cmd("save-all")
        logging.info("Saved!")
        return res

    def ping(self):
        self.say("Ping test")
        
    def say(self, message: str):
        logging.info(f"Sending message: {message}")
        return self._cmd(f"say {message}")

    def announce_all_channels(self, message: str):
        """Send a message to the server and discord"""
        logging.info(f"Sending message: {message}")
        self.discord_messenger.send_webhook_message(message)
        return self.say(message)

    def list(self):
        return self._cmd("list")

    def get_player_names(self) -> List[str]:
        [_, names_str] = self.list().split(": ")
        names_list = [re.sub(pattern=r"\\n'", string=n, repl="").strip()
                      for n in names_str.split(",") if not not n]
        logging.debug(names_list)
        return names_list

    def get_player_count(self) -> int:
        players  = self.get_player_names()
        print(players)
        count = len(players)
        logging.info(f"{count} player(s) online.")
        return count

    def init_shutdown(self, quiet=False, minutes=1, force=False):
        player_count = self.get_player_count()

        if player_count and not force:
            return -1
        
        if not quiet:
            logging.info("Sending announcement...")
            self.announce(
                f'Good evening, the MC MC server will be shutting down in {minutes} minute(s). See you tomorrow.')
            remaining_seconds = minutes*60 - 10
            sleep(remaining_seconds)
            for second in range(0, 10):
                self.say(f"{10-second}...")
                sleep(1)

        self.say("Goodbye!")
        self.shutdown()

        return minutes

    def shutdown(self):
        self.save()
        self.docker_wrapper.shutdown()
        