import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DISCORD_URL = os.getenv("DISCORD_URL")


class INotificationService:
    async def send_notification(self, notification: str):
        ...


class DiscordNotificationService(INotificationService):

    async def send_notification(self, notification: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_URL, data={"content": notification},
                                    headers={"Authorization": f"Bot {BOT_TOKEN}"}) as response:
                if response.status != 200:
                    raise Exception("Failed to send notification to Discord")
                return
