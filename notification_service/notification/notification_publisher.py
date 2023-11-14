from notification.notification_subscriber import INotificationSubscriber


class NotificationPublisher:
    """Publisher for notifications."""

    subscribers: list[INotificationSubscriber]

    def __init__(self):
        self.subscribers: list[INotificationSubscriber] = []

    async def publish(self, message: str) -> None:
        """Publish a notification to all subscribers."""
        for subscriber in self.subscribers:
            await subscriber.notify(message)

    def add_subscriber(self, subscriber: INotificationSubscriber):
        """Add a subscriber to the subscriber list."""
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: INotificationSubscriber):
        """Remove a subscriber from the subscriber list."""
        self.subscribers.remove(subscriber)
