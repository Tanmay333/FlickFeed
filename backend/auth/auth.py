from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.model_package.user import User
from redis_config import redis_client  # Import Redis connection

#  Secret Key & Algorithm (Use an environment variable in production)
SECRET_KEY = "your_secret_key"  # Replace with a secure secret!
ALGORITHM = "HS256"

# ⏳ Token Expiry Times
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7  

#  Password Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_password_hash(password: str) -> str:
    """Hashes a given password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the provided password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

#  Token Creation Functions
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Creates an access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Creates a refresh token valid for multiple days."""
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

#  OAuth2 Scheme for Token Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#  Get Current Token
def get_current_token(token: str = Depends(oauth2_scheme)) -> str:
    """Extracts the token from the request."""
    return token

#  Get Current User
def get_current_user(token: str = Depends(get_current_token), db: Session = Depends(get_db)) -> User:
    """
    Decodes the JWT token, fetches the user from the database, and returns the user object.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")  
        
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token: Missing subject (sub)")

        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired")

#  User Login Function (Route)
@router.post("/login")
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

#  Middleware: Restrict access based on user roles
def role_required(allowed_roles: list):
    """
    Middleware to restrict access based on user roles.
    """
    def check_role(current_user: User = Depends(get_current_user)):  
        if current_user.role not in allowed_roles:  
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return current_user  
    
    return check_role

@router.post("/logout")
async def logout(user: dict = Depends(get_current_user), token: str = Depends(get_current_token)):
    """
    Logout the user by blacklisting the token.
    """
    try:
        # Store token in Redis with expiration time
        redis_client.setex(token, 900, "blacklisted")  # 15 min expiration

        return {"message": "Successfully logged out"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )
