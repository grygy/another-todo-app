from uuid import UUID


class TodoCreate:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description


class Todo(TodoCreate):
    def __init__(self, title: str, description: str, id: UUID = None):
        super().__init__(title, description)
        self.id = id
