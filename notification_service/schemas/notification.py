from pydantic import BaseModel


class NotificationSchema(BaseModel):
    message: str
