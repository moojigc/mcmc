from dataclasses import dataclass, field, make_dataclass
import logging
from env import MOOJIG_DISCORD_USER_ID
from interactions.Message import Message
from interactions.Member import Member
from interactions.User import User
from interactions.constants import InteractionRequestType, InteractionResponseType
from interactions.my_utils import initDataclass
from interactions.respond import respond_to_interaction
import requests


@dataclass
class Interaction:
    def __post_init__(self):
        if self.member:
            self.member = initDataclass(Member, self.member)
        if self.data:
            self.data = initDataclass(Message, self.data)
        if self.user:
            self.user = initDataclass(User, self.user)
        self.type = InteractionRequestType(self.type)

    id: str
    application_id: str
    token: str
    type: InteractionRequestType
    version: int
    channel_id: str = None
    guild_id: str = None
    guild_locale: str = None
    locale: str = None
    member: Member = None
    data: Message = None
    user: User = None

    @property
    def is_server_off_command(self) -> bool:
        return self.data.name == 'server' and self.data.options[0].value == "off"

    @property
    def is_restricted_command(self) -> bool:
        return self.is_server_off_command

    @property
    def is_user_moojig(self) -> bool:
        if self.user:
            return self.user.id == MOOJIG_DISCORD_USER_ID
        elif self.member:
            return self.member.user.id == MOOJIG_DISCORD_USER_ID
        else:
            return False

    @property
    def get_user(self):
        if self.user:
            return self.user
        elif self.member:
            return self.member.user
        else:
            return None

    @property
    def __get_follow_up_url(self):
        return f"https://discord.com/api/v8/webhooks/{self.application_id}/{self.token}"

    pending_follow_up = None

    def make_follow_up_response(self, message: str = None):
        discord_res = requests.post(
            url=self.__get_follow_up_url, json={
                "content": message or "Sorry guy, not sure what happened. Try again in a minute."
            })
        # print(discord_res.json())
        return discord_res
