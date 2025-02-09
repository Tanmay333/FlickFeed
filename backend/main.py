from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import SessionLocal, Base, engine, User
from pydantic import BaseModel

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for user creation and update
class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str
    email: str

# Create a new user
@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

# Read user by ID
@app.get("/users/{user_id}", response_model=dict)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}

# Update user by ID
@app.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = user_update.username
    user.email = user_update.email
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}

# Delete user by ID
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Add a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to CineVerse API!"}
