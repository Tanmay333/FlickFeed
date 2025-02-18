# import sys
# import os

# # Add backend to Python's module search path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from database import Base, engine  # ✅ Import database setup
# from model_package.user import User  # ✅ Import models explicitly
# from model_package.feed import Feed  # ✅ Import models explicitly

# # 🚨 Check if models are loading
# print("🔍 Creating database tables...")

# # Create tables
# Base.metadata.create_all(bind=engine)

# print("✅ Database tables created successfully!")

import sys
import os

# Add backend to Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine
from model_package.user import User
from model_package.feed import Feed

from sqlalchemy import inspect

print("🔍 Creating database tables...")

# Create tables
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")

# 🚨 Check if tables exist
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"🔎 Found tables: {tables}")

import logging
from backend.database import Base, engine

# Enable SQLAlchemy logs
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

print("🔍 Creating database tables...")
Base.metadata.create_all(bind=engine)  # This should log SQL queries
print("✅ Database tables created successfully!")

import logging
from backend.database import Base, engine

# Enable SQLAlchemy logs
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

print("🚨 Dropping existing tables (if any)...")
Base.metadata.drop_all(bind=engine)  # 🚨 Force delete all tables

print("🔍 Creating database tables...")
Base.metadata.create_all(bind=engine)  # 🚀 Recreate them from scratch

print("✅ Database tables created successfully!")
