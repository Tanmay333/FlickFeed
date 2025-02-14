from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.auth.auth import get_current_user
from backend.database import get_db
from backend.schemas.feed import FeedCreate
from backend.model_package.feed import Feed
from backend.model_package.user import User

router = APIRouter()

@router.post("/create_feed")
def create_feed(feed: FeedCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_feed = Feed(title=feed.title, content=feed.content, user_id=current_user.id)
    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)
    return {"message": "Feed created successfully", "feed": new_feed}

@router.get("/feeds")
def get_feeds(db: Session = Depends(get_db)):
    feeds = db.query(Feed).all()
    return feeds
