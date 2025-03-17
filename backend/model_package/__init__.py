# ✅ Instead of modifying `tables`, use declarative inheritance
from database import Base  # Ensure Base is correctly imported

class CombinedBase(Base):
    __abstract__ = True  # This prevents table creation for this base
    metadata = Base.metadata  # Use the metadata from Base
