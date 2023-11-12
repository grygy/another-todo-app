from crud.base_crud import BaseCRUD
from db.db_models.todo import TodoInDb
from db.todo_repository import TodoRepository


class TodoCRUD(BaseCRUD[TodoInDb, TodoInDb]):
    def __init__(self, repository: TodoRepository):
        super().__init__(repository)
