from sqlalchemy import Column, Integer, String
from backend.database import Base  # Importing Base from database.py

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
