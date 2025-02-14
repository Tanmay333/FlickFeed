from fastapi import APIRouter, Depends, HTTPException
from backend.model_package.feed import Feed
from backend.schemas.feed import FeedCreate
from backend.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/create")
def create_feed(feed: FeedCreate, db: Session = Depends(get_db)):
    db_feed = Feed(**feed.dict())
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed

@router.get("/", response_model=List[Feed])
def get_feeds(db: Session = Depends(get_db)):
    feeds = db.query(Feed).all()
    return feeds
