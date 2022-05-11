import os
import requests


def main():
    APP_ID = os.environ.get("MOOJCRAFT_APPLICATION_ID")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DISCORD_SERVER_ID = 973268273493868574
    URLS = [f"https://discord.com/api/v8/applications/{APP_ID}/commands",
            f"https://discord.com/api/v8/applications/{APP_ID}/guilds/{DISCORD_SERVER_ID}/commands"]

    # This is an example CHAT_INPUT or Slash Command, with a type of 1
    commands = [
        {
            "type": 1,
            "name": "ping",
            "description": "Check if server is still up",
        },
        {
            "type": 1,
            "name": "server",
            "description": "Send a command to the MC MC server.",
            "options": [
                {
                    "name": "command",
                    "description": "What'll it be, pardner?",
                    "type": 3,
                    "required": True,
                    "choices": [
                           {
                               "name": "Turn on",
                               "value": "on"
                           },
                        {
                               "name": "Turn off",
                               "value": "off"
                           }
                    ]
                },
            ]
        },
        {
            "type": 1,
            "name": "msg",
            "description": "Send a message to the players on the MC server!.",
            "options": [
                {
                    "type": 3,
                    "name": "message",
                    "description": "Everyone online will see this!"
                }
            ]
        },
        {
            "type": 1,
            "name": "players",
            "description": "See how many people are online.",
        }
    ]

    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }
    for command in commands:
        for URL in URLS:
            res = requests.post(URL, headers=headers, json=command)
            print(res.json())


if __name__ == "__main__":
    main()
