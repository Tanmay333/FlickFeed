from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db  # ✅ Ensure correct import path
from backend.model_package.review_models import Review  # ✅ Correct import path
from backend.schemas.review_schema import ReviewCreate, ReviewResponse  # ✅ Correct import path
from typing import List

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# Create a new review
@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(**review.model_dump())  # ✅ Ensure correct FastAPI version for `.model_dump()`
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Fetch all reviews
@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

# Fetch a single review by ID
@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# Update a review
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_data: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review_data.model_dump().items():  # ✅ Ensure correct FastAPI version
        setattr(review, key, value)

    db.commit()
    db.refresh(review)
    return review

# Delete a review
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
