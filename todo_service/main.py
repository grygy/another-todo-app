from fastapi import FastAPI
from starlette.testclient import TestClient

from routers import todo

app = FastAPI()

app.include_router(todo.router)

client = TestClient(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
