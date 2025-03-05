from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.model_package.user import User  # Import User model
from backend.auth import get_current_user  # Import get_current_user function
from backend.database import get_db  # Import get_db function
from backend.model_package.user import User  # Import User model
from pydantic import BaseModel
from typing import List  # Import List for type hinting


# Define RoleUpdate model
class RoleUpdate(BaseModel):
    email: str
    new_role: str

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


@router.put("/admin/update-role")
def update_user_role(
    role_data: RoleUpdate,  
    db: Session = Depends(get_db),  
    current_user: User = Depends(get_current_user)  
):
    # Check if the requester is an admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Fetch the user whose role needs to be changed
    user_to_update = db.query(User).filter(User.email == role_data.email).first()

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the role
    user_to_update.role = role_data.new_role
    db.commit()

    return {"message": "User role updated successfully"}