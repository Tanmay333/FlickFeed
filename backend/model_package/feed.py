from sqlalchemy import Column, Integer, String, Text
from backend.database import Base  

class Feed(Base):
    __tablename__ = "feeds"  

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
