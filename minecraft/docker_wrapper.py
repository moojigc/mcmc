import logging

import docker 

from time import sleep


DEFAULT_CONTAINER_NAME = "docker_mc_1"

class DockerAsleepError(Exception):
    pass
class DockerExecError(Exception):
    pass

class DockerWrapper:
    """interact with docker container"""

    def __init__(self, container_name=DEFAULT_CONTAINER_NAME) -> None:
        self.client = docker.from_env()
        self.container_name = container_name

        try:
            self.minecraft_server = self.client.containers.get(self.container_name)
        except Exception:
            raise DockerAsleepError("MC MC Server is not running!")

    def startup(self):
        self.minecraft_server.start()
        logging.info(f"{self.container_name} started!")
        return "MC MC MC Server starting..."

    def shutdown(self, delay: int):
        logging.info(
            f"Stopping {self.container_name} container in {delay} seconds...")
        self.minecraft_server.stop(timeout=delay)
        logging.info(f"{self.container_name} stopped!")
        return "MC MC MC Server stopping..."