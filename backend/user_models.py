from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """
    User model representing registered users in the system.
    """
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # Ensures existing tables can be extended if needed

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # Ensures default role is always set

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role})>"

# establish the relationship
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")