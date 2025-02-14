from sqlalchemy import Column, Integer, String
from backend.database import Base  # ✅ Ensure Base is imported correctly

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
