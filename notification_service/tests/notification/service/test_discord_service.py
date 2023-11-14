import unittest

from notification.service.notification_service import DiscordNotificationService


class TestDiscordNotificationService(unittest.IsolatedAsyncioTestCase):

    async def test_discord_send_notification(self):
        discord_service = DiscordNotificationService()
        try:
            await discord_service.send_notification("TEST: Hello World")
        except Exception as e:
            self.fail(f"Failed to send Discord notification: {e}")


if __name__ == '__main__':
    unittest.main()
