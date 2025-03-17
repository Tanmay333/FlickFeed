from sqlalchemy import Column, Integer, String
from backend.database import Base  # ✅ Use absolute import

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Ensure password is hashed
    role = Column(String, default="user")  # ✅ Add role field
