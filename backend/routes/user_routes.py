from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.model_package.user import User  # Import User model
from pydantic import BaseModel
from typing import List  # Import List for type hinting

router = APIRouter()

# ✅ Pydantic model for request validation
class UserCreate(BaseModel):
    username: str
    email: str

# ✅ Create a new user
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ✅ Retrieve all users (Add this function)
@router.get("/", response_model=List[UserCreate])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# ✅ Retrieve a single user by ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return user

# ✅ Update user details
@router.put("/{user_id}")
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    # Check if user exists
    if not user:
        return {"error": "User not found"}
    
    # Update user details
    user.username = updated_user.username
    user.email = updated_user.email

    db.commit()  # Save changes
    db.refresh(user)  # Refresh the object to return updated data
    return user

# Delete user details

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}
