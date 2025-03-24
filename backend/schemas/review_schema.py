from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(..., ge=1, le=5)  # Restrict rating between 1 and 5
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  #  Ensure ORM compatibility
