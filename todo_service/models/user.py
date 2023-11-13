from sqlalchemy import Column, String, Uuid

from models.base import Base


class UserInDb(Base):
    __tablename__ = "user"

    id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    username = Column(String())
    hashed_password = Column(String())

    def __repr__(self):
        return f"<UserInDb(id={self.id}, username={self.username}, hashed_password={self.hashed_password})>"
