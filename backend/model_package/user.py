from sqlalchemy import Column, Integer, String
from backend.database import Base  # ✅ Ensure this is correct

class User(Base):
    __tablename__ = "users"  # ✅ Ensure table name is set

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
