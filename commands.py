#!/usr/bin/env python3
import time
from datetime import date, datetime, timedelta
import os
import logging
import argparse

from minecraft.decorators.command_bank import CommandBank
from minecraft.discord import DiscordMessenger
from minecraft.rcon import Rcon
from minecraft.docker_wrapper import DockerWrapper

from env import DISCORD_WEBHOOK_URL

command_bank = CommandBank()


class Automation:
    def __init__(self, docker_wrapper: DockerWrapper, rcon: Rcon) -> None:
        self.docker_wrapper = docker_wrapper
        self.rcon = rcon

    @command_bank.command_handler()
    def on(self):
        if self.docker_wrapper.minecraft_server.status == 'running':
            return "MC MC Server is already on."
        else:
            self.docker_wrapper.startup()
            return "MC MC Server is starting!"

    @command_bank.command_handler()
    def off(self):
        if self.docker_wrapper.minecraft_server.status == 'running':
            minutes = self.rcon.init_shutdown()
            return f"MC MC will shutdown in {minutes} minute(s)."
        else:
            return "MC MC server is already off."

    @command_bank.command_handler()
    def ping(self):
        self.rcon.say("Ping test")
        return "Pong! MC MC server is up and running."

    @command_bank.command_handler()
    def players(self):
        count = self.rcon.get_player_count()
        logging.debug("count: %d", count)
        return f"{count} {'player' if count == 1 else 'players'} currently online."

    @command_bank.command_handler()
    def list(self):
        return self.rcon.get_player_names()

    @command_bank.command_handler()
    def chat(self, message: str, player_name=''):
        """Send discord msg"""
        if player_name:
            msg = f"[DISCORD {player_name}]: {message}"
        else:
            msg = f"[SYSTEM ANNOUNCEMENT]: {message}"
        self.rcon.say(
            msg)
        return f"We sent: {msg}"

    @command_bank.command_handler()
    def announce(self, message: str):
        self.rcon.discord_messenger.send_webhook_message(message)
        logging.debug(self.rcon.discord_messenger.webhook_url)
        return "Message sent."

    @command_bank.command_handler()
    def reboot(self):
        self.rcon.shutdown()
        os.system("sudo reboot now")
        return "MC MC server rebooting!"

    @command_bank.command_handler()
    def backup(self, backup_dir: str, minecraft_dir: str):
        os.system(f"mv {backup_dir} {backup_dir}_old/")
        now = date.today().strftime("%Y%m%d")
        logging.debug("Running tar backup...")
        os.system(
            f"tar -zcf {backup_dir}/minecraft_{now}.tgz {minecraft_dir}")
        logging.debug("tar backup done.")
        self.cleanup_backups(backup_dir, (datetime.now() - timedelta(days=7)).strftime('%Y%m%d'))

    @command_bank.command_handler()
    def cleanup_backups(self, backup_dir: str, before_date: str):
        files = os.listdir(backup_dir)
        for file in files:
            try:
                _, date_string = file.split('_')
                date_string = date_string.split('.')[0]
            except ValueError:
                return

            date = datetime.strptime(date_string, '%Y%m%d')
            before_date = datetime.strptime(before_date, '%Y%m%d')
            logging.debug(f"{date=} {before_date=}")
            if date < before_date:
                logging.info(f"Deleting {file}")
                os.remove(os.path.join(backup_dir, file))

    @command_bank.command_handler()
    def save(self):
        return self.rcon.save()

def create_automator() -> Automation:
    docker_wrapper = DockerWrapper()
    rcon = Rcon(
        docker_wrapper,
        discord_messenger=DiscordMessenger(DISCORD_WEBHOOK_URL)
    )

    return Automation(docker_wrapper, rcon)

def create_command_bank() -> CommandBank:
    """Creates DockerWrapper and Rcon objects, passes them to `command_bank.execute()`"""
    docker_wrapper = DockerWrapper()
    rcon = Rcon(
        docker_wrapper,
        discord_messenger=DiscordMessenger(DISCORD_WEBHOOK_URL)
    )

    command_bank.command_cls(Automation(docker_wrapper, rcon))

    return command_bank


def send_mc_command(bank: CommandBank, command: str, **kwargs) -> str:
    return bank.execute(command, **kwargs)


if __name__ == "__main__":

    command_bank = create_command_bank()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, help=', '.join(command_bank.commands))
    parser.add_argument('--quiet', action=argparse.BooleanOptionalAction)
    parser.add_argument('--message', type=str)
    parser.add_argument('--backup-dir', type=str)
    parser.add_argument('--minecraft-dir', type=str)
    parser.add_argument('--before-date', type=str)
    parser.add_argument('--log', type=str, default=logging.DEBUG)

    args = parser.parse_args()

    if args.command not in command_bank.commands:
        newline = "\n\t"
        print(f"command must be one of:\n\t{newline.join(command_bank.commands)}")
        exit(1)

    logging.getLogger().setLevel(args.log)
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s')
    print(send_mc_command(command_bank, **args.__dict__))


