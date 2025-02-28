from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.auth.jwt_handler import create_access_token, create_refresh_token, decode_access_token
from backend.database import get_db
from backend.schemas.auth import UserCreate, UserLogin
from backend.auth.auth import verify_password, get_password_hash
from backend.user_models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/protected")
def protected_route(token: str = Depends(decode_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == token["sub"]).first()
    return {"message": f"Hello, {user.username}. You have accessed a protected route!"}