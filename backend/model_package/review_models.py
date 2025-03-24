from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  # Foreign key to users table
    movie_id = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)

    user = relationship("User", back_populates="reviews")  # Establish relationship with User model

  