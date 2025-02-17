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
