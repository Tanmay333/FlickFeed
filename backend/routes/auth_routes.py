# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from pydantic import BaseModel

# from backend.auth.jwt_handler import create_access_token, create_refresh_token
# from backend.database import get_db
# from backend.schemas.auth import UserCreate, UserLogin
# from backend.auth.auth import verify_password, get_password_hash
# from backend.user_models import User


# router = APIRouter()

# SECRET_KEY = "your_secret_key_here"
# ALGORITHM = "HS256"

# # ✅ Fixed Signup Route
# @router.post("/auth/signup", tags=["Authentication"])
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = get_password_hash(user.password)
#     new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return {"message": "User registered successfully"}

# # ✅ Fixed Login Route
# @router.post("/auth/login", tags=["Authentication"])
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_credentials.email).first()
    
#     if not user or not verify_password(user_credentials.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     access_token = create_access_token(data={"sub": user.email})
#     refresh_token = create_refresh_token(data={"sub": user.email})

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer"
#     }

# # ✅ Fixed Refresh Token Route
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @router.post("/auth/refresh", tags=["Authentication"])
# def refresh_token(refresh_token: str):
#     try:
#         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")

#         new_access_token = create_access_token(data={"sub": email})

#         return {"access_token": new_access_token, "token_type": "bearer"}

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.auth.jwt_handler import create_access_token, create_refresh_token
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
