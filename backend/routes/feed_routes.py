from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_feeds():
    return {"feeds": []}
