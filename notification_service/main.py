from fastapi import FastAPI

from routers import notification

app = FastAPI()

app.include_router(notification.router)
