import os

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DISCORD_URL = os.getenv("DISCORD_URL")


class INotificationService:
    def send_notification(self, notification: str):
        ...


class DiscordNotificationService(INotificationService):

    def send_notification(self, notification: str):
        response = requests.post(DISCORD_URL,
                                 data={"content": notification}, headers={"Authorization": f"Bot {BOT_TOKEN}"})

        if response.status_code != 200:
            raise Exception("Failed to send notification to Discord")
