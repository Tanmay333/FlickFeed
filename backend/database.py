from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLite Database URL
DATABASE_URL = "sqlite:///backend/flickfeed.db"

# Create an engine that connects to the SQLite database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for database models
Base = declarative_base()

# Dependency function to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
