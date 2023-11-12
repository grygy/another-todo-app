from crud.base_crud import BaseCRUD
from db.todo_repository import TodoRepository
from models.todo import Todo, TodoCreate


class TodoCRUD(BaseCRUD[Todo, TodoCreate]):
    def __init__(self, repository: TodoRepository):
        super().__init__(repository)
