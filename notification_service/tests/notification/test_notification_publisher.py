import unittest

from notification.notification_publisher import NotificationPublisher
from notification.notification_subscriber import DiscordSubscriber
from tests.notification.test_notification_subscriber import MockDiscordService


class TestNotificationPublisher(unittest.IsolatedAsyncioTestCase):
    def test_publisher_add_subscriber(self):
        mock_discord_service = MockDiscordService()
        dc_subscriber = DiscordSubscriber(mock_discord_service)
        publisher = NotificationPublisher()
        publisher.add_subscriber(dc_subscriber)
        self.assertEqual(len(publisher.subscribers), 1)

    def test_publisher_remove_subscriber(self):
        mock_discord_service = MockDiscordService()
        dc_subscriber = DiscordSubscriber(mock_discord_service)
        publisher = NotificationPublisher()
        publisher.add_subscriber(dc_subscriber)
        self.assertEqual(len(publisher.subscribers), 1)
        publisher.remove_subscriber(dc_subscriber)
        self.assertEqual(len(publisher.subscribers), 0)

    async def test_publisher_notify(self):
        mock_discord_service = MockDiscordService()
        dc_subscriber = DiscordSubscriber(mock_discord_service)
        publisher = NotificationPublisher()
        publisher.add_subscriber(dc_subscriber)
        await publisher.publish("Hello World")
        self.assertEqual(mock_discord_service.get_last_message(), "Hello World")


if __name__ == '__main__':
    unittest.main()
