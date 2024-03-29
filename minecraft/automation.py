#!/usr/bin/env python3

import asyncio
import re
import requests
from typing import List, Literal
from docker import from_env, errors as docker_errors
from docker.models.containers import Container
import logging
import argparse

from env import DISCORD_WEBHOOK_URL


def send_webhook_message(message: str):
    if __name__ == "__main__":
        res = requests.post(DISCORD_WEBHOOK_URL, json={
            "content": message,
        })
        logging.info(
            f"DiscordMessenger.send_message: {res.status_code} {res.content}")
        return res


class DockerExecError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message


class DockerWrapper:
    MC_CONTAINER_NAME = "docker_mc_1"

    def __init__(self) -> None:
        self.client = from_env()
        try:
            self.minecraft_server: Container = list(filter(
                lambda c: c.name == DockerWrapper.MC_CONTAINER_NAME, self.client.containers.list(all=True)))[0]
        except Exception:
            raise DockerExecError(message="MC MC Server is not running!")

    def startup(self):
        self.minecraft_server.start()
        logging.info(f"{DockerWrapper.MC_CONTAINER_NAME} started!")

    def shutdown(self, delay: int):
        logging.info(
            f"Stopping {DockerWrapper.MC_CONTAINER_NAME} container in {delay} seconds...")
        self.minecraft_server.stop(timeout=delay)
        logging.info(f"{DockerWrapper.MC_CONTAINER_NAME} stopped!")


class Rcon:
    @staticmethod
    def clean_msg(msg: str):
        msg = re.sub(pattern=r"'", string=msg, repl=r"\'")
        msg = re.sub(pattern=r"\"", string=msg, repl=r"\"")
        return msg

    def __init__(self, docker_wrapper: DockerWrapper) -> None:
        self.docker_wrapper = docker_wrapper

    def __cmd(self, cmd_str: str) -> str:
        try:
            result = self.docker_wrapper.minecraft_server.exec_run(
                f"rcon-cli {cmd_str}")
            if result.exit_code > 0:
                raise DockerExecError(message=str(result.output))
            string_res = str(result.output)
            if string_res is not None and "connect" in string_res:
                raise DockerExecError(message="Server is still starting...")
            return string_res
        except docker_errors.APIError:
            raise DockerExecError(message="MC MC server is asleep.")

    def say(self, message: str):
        logging.info(f"Sending message: {message}")
        return self.__cmd(f"say {message}")

    def dual_message(self, message: str):
        logging.info(f"Sending message: {message}")
        send_webhook_message(message)
        return self.say(message)

    def list(self):
        return self.__cmd("list")

    def get_player_names(self) -> List[str]:
        [_, names_str] = self.list().split(": ")
        names_list = [re.sub(pattern=r"\\n'", string=n, repl="").strip()
                      for n in names_str.split(",")]
        logging.debug(names_list)
        return list(filter(lambda x: bool(x), names_list))

    def get_player_count(self) -> int:
        return len(self.get_player_names())

    def init_shutdown(self):
        minutes = 1
        player_count = self.get_player_count()
        logging.info(f"{player_count} player(s) online.")
        if player_count:
            logging.info("Sending announcement...")
            minutes = 30
            self.dual_message(
                f'Good evening, the MC MC server will be shutting down in {minutes} minute(s). See you tomorrow.')
        self.docker_wrapper.shutdown(minutes)
        return minutes


def send_mc_command(command: Literal["on", "off", "ping", "players", "send_message"], **kwargs) -> str:
    # init some objects and config
    docker_wrapper = DockerWrapper()
    rcon = Rcon(docker_wrapper)

    if command == "on":
        if docker_wrapper.minecraft_server.status == 'running':
            return "MC MC Server is already on."
        else:
            docker_wrapper.startup()
            return "MC MC Server starting! Please wait approximately 2 minutes."
    elif command == "off":
        if docker_wrapper.minecraft_server.status == 'running':
            minutes = rcon.init_shutdown()
            return f"MC MC will shutdown in {minutes} minute(s)."
        else:
            return "MC MC server is already off."
    elif command == "ping":
        rcon.say("Ping test")
        return "Pong! MC MC server is up and running."
    elif command == "players":
        count = rcon.get_player_count()
        print(count)
        return f"{count} {'player' if count == 1 else 'players'} currently online."
    elif command == "send_message":
        msg = f"{kwargs['source']} message from {kwargs['name']}: {Rcon.clean_msg(kwargs['message'])}"
        try:
            rcon.say(
                msg)
        except ValueError as e:
            print("this shit failed")
            raise e
        return f"We sent: {msg}"
    else:
        raise TypeError(
            f"command must be one of: on, off, ping, players, send_message")


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO,
                        filename='automation.log', encoding='utf-8'
                        )
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    args = parser.parse_args()
    send_mc_command(args.command)
