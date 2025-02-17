from sqlalchemy import Column, Integer, String, Text
from backend.database import Base  # ✅ Ensure this is correct

class Feed(Base):
    __tablename__ = "feeds"  # ✅ Ensure table name is set

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
