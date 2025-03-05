from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.model_package.user import User

# 🔐 Secret Key & Algorithm (Use an environment variable in production)
SECRET_KEY = "your_secret_key"  # Replace with a secure secret!
ALGORITHM = "HS256"

# ⏳ Token Expiry Times
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7  

# 🔑 Password Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a given password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the provided password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# 🎟️ Token Creation Functions
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Creates an access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Creates a refresh token valid for multiple days."""
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

# 🚀 OAuth2 Scheme for Token Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
  

# 🔍 Get Current User
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decodes the JWT token, fetches the user from the database, and returns the user object.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")  # ✅ Extracts `email` instead of `user_id`
        
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token: Missing subject (sub)")

        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired")

# ✅ User Login Function
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    """
    Authenticates the user and returns access & refresh tokens.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
