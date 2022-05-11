#!/usr/bin/env python3

import re
import requests
from typing import List, Literal
from docker import from_env, errors as docker_errors
from docker.models.containers import Container
import logging
import argparse


class DiscordMessenger:
    URL = "https://discord.com/api/webhooks/973268794208301077/RtP45AFmYEWRYabIkAY-3tozTsG1Qcjw13NNOa8tBeAJ7nZnQfWfHX5B7l6LqdJiE1V0"

    def send_message(self, message: str):
        pass
        # res = requests.post(DiscordMessenger.URL, json={
        #     "content": message,
        # })
        # logging.info(
        #     f"DiscordMessenger.send_message: {res.status_code} {res.content}")
        # return res


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
    def __init__(self, docker_wrapper: DockerWrapper, discord_messenger: DiscordMessenger) -> None:
        self.docker_wrapper = docker_wrapper
        self.discord_messenger = discord_messenger

    def __cmd(self, cmd_str: str) -> str:
        try:
            result = self.docker_wrapper.minecraft_server.exec_run(
                f"rcon-cli {cmd_str}")
            if result.exit_code > 0:
                raise DockerExecError(message=result.output)
            return str(result.output)
        except docker_errors.APIError:
            raise DockerExecError(message="MC MC server is asleep.")

    def say(self, message: str):
        logging.info(f"Sending message: {message}")
        return self.__cmd(f"say {message}")

    def dual_message(self, message: str):
        logging.info(f"Sending message: {message}")
        self.discord_messenger.send_message(message)
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
            self.dual_message(
                f'Good evening, the MC MC server will be shutting down in {minutes} minute(s). See you tomorrow.')
        self.docker_wrapper.shutdown(60*minutes)


def main(command: Literal["on", "off", "ping", "count", "send_message"], **kwargs) -> str:
    # init some objects and config
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO,
                        # filename='minecraft_automation.log', encoding='utf-8'
                        )
    docker_wrapper = DockerWrapper()
    dm = DiscordMessenger()
    rcon = Rcon(docker_wrapper, dm)

    if command == "on":
        if docker_wrapper.minecraft_server.status == 'running':
            return "MC MC Server is already on."
        else:
            docker_wrapper.startup()
            return "MC MC Server starting! Please wait approximately 2 minutes."
    elif command == "off":
        if docker_wrapper.minecraft_server.status == 'running':
            rcon.init_shutdown()
            return "MC MC shutting down..."
        else:
            return "MC MC server is already off."
    elif command == "ping":
        rcon.say("Ping test")
        return "Pong! MC MC server is up and running."
    elif command == "count":
        count = rcon.get_player_count()
        print(count)
        return f"{count} {'player' if count == 1 else 'players'} currently online."
    elif command == "send_message":
        msg = f"{kwargs['source']} message from {kwargs['name']}: {kwargs['message']}"
        rcon.say(
            msg)
        return f"We sent: {msg}"
    else:
        raise TypeError(
            f"command must be one of: on, off, ping, count, message")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    args = parser.parse_args()
    main(args.command)
