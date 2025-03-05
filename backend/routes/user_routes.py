from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.model_package.user import User  # Import User model
from backend.auth import get_current_user, role_required  # Import auth utilities
from backend.database import get_db  # Import get_db function
from pydantic import BaseModel
from typing import List

# Define Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str


class RoleUpdate(BaseModel):
    email: str
    new_role: str

router = APIRouter()

# Create a new user
@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Retrieve all users
@router.get("/", response_model=List[UserCreate])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Retrieve a single user by ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#  Update user details
@router.put("/{user_id}")
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = updated_user.username
    user.email = updated_user.email
    db.commit()
    db.refresh(user)
    return user

# Retrieve the current authenticated user
@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

#  Delete a user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}

#  Admin: Update user role
@router.put("/admin/update-role")
def update_user_role(
    role_data: RoleUpdate,  
    db: Session = Depends(get_db),  
    current_user: User = Depends(role_required(["admin"]))  #  Restrict to admin users
):
    user_to_update = db.query(User).filter(User.email == role_data.email).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_update.role = role_data.new_role
    db.commit()
    return {"message": "User role updated successfully"}
