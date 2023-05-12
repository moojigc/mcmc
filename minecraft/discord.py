import logging
import requests

logger = logging.getLogger()

class DiscordMessenger:    
    def __init__(self, webhook_url:str) -> None:
        self.webhook_url = webhook_url

    def send_webhook_message(self, message: str):
        if __name__ == "__main__":
            res = requests.post(self.webhook_url, json={
                "content": message,
            })
            logger.info(
                f"DiscordMessenger.send_message: {res.status_code} {str(res.content)}")
            return res