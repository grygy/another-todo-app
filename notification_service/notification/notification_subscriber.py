from notification.service.notification_service import INotificationService


class INotificationSubscriber:
    """Subscriber for notifications."""

    def notify(self, message: str) -> None:
        """Notify the subscriber about a notification."""
        ...


class DiscordSubscriber(INotificationSubscriber):
    """Subscriber for Discord notifications."""
    notification_service: INotificationService

    def __init__(self, notification_service: INotificationService):
        self.notification_service = notification_service

    def notify(self, message: str) -> None:
        """Notify the subscriber about a notification."""
        self.notification_service.send_notification(message)
