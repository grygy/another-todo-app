import unittest

from notification.notification_subscriber import DiscordSubscriber
from notification.service.notification_service import INotificationService


class MockDiscordService(INotificationService):

    def __init__(self):
        self.last_message = ""

    async def send_notification(self, message: str) -> None:
        self.last_message = message

    def get_last_message(self) -> str:
        return self.last_message


class TestDiscordNotify(unittest.IsolatedAsyncioTestCase):
    async def test_discord_notify(self):
        mock_discord_service = MockDiscordService()
        dc_subscriber = DiscordSubscriber(mock_discord_service)
        await dc_subscriber.notify("Hello World")
        self.assertEqual(mock_discord_service.get_last_message(), "Hello World")


if __name__ == '__main__':
    unittest.main()
