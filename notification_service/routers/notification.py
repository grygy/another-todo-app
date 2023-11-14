from fastapi import APIRouter

from notification.notification_publisher import NotificationPublisher
from notification.notification_subscriber import DiscordSubscriber
from notification.service.notification_service import DiscordNotificationService
from schemas.notification import NotificationSchema

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"description": "Not found"}},
)

discord_subscriber = DiscordSubscriber(DiscordNotificationService())
notification_publisher = NotificationPublisher()
notification_publisher.add_subscriber(discord_subscriber)


@router.post("/")
async def notify(
        notification: NotificationSchema
):
    """Send notification to Discord"""
    await notification_publisher.publish(notification.message)
