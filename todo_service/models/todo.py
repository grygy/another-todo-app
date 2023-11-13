from sqlalchemy import Column, String, Uuid, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base import Base


class TodoInDb(Base):
    __tablename__ = "todo"

    id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    title = Column(String())
    description = Column(String())
    finished = Column(DateTime(timezone=True), nullable=True)

    user_id = Column(Uuid(as_uuid=True), ForeignKey('user.id'))

    user = relationship("UserInDb", back_populates="todos")

    def __repr__(self):
        return f"<TodoInDb(id={self.id}, title={self.title}, description={self.description})>"
