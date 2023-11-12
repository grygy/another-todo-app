from crud.base_crud import BaseCRUD
from db.todo_repository import TodoRepository
from models.todo import TodoInDb


class TodoCRUD(BaseCRUD[TodoInDb, TodoInDb]):
    def __init__(self, repository: TodoRepository):
        super().__init__(repository)
