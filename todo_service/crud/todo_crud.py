from crud.base_crud import BaseCRUD
from models.todo import Todo, TodoCreate


class TodoCRUD(BaseCRUD[Todo, TodoCreate]):
    def __init__(self, db: list[Todo]):
        super().__init__(db)
