from sqlalchemy import Column, String, Uuid

from models.base import Base


class TodoInDb(Base):
    __tablename__ = "todo"

    id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    title = Column(String())
    description = Column(String())

    def __repr__(self):
        return f"<TodoInDb(id={self.id}, title={self.title}, description={self.description})>"
