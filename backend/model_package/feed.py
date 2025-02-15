from sqlalchemy import Column, Integer, String
from backend.database import Base  # Import the Base from database.py

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author = Column(String)
    likes = Column(Integer, default=0)
