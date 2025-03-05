from pydantic import BaseModel
from backend.schemas.role_schema import RoleUpdate  

class RoleUpdate(BaseModel):
    email: str
    new_role: str
