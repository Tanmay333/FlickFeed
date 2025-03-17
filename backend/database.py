from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database URL (Ensure correct relative path)
DATABASE_URL = "sqlite:///./flickfeed.db"  # Added './' to ensure proper relative path handling

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for ORM models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
