from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.model_package.feed import Feed  

router = APIRouter()

@router.get("/")
def get_feeds(db: Session = Depends(get_db)):
    feeds = db.query(Feed).all()  # Fetch all feeds from PostgreSQL
    return {"feeds": feeds}
