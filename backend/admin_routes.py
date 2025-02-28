from fastapi import APIRouter, Depends
from backend.auth.role_checker import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard", dependencies=[Depends(require_role("admin"))])
def admin_dashboard():
    return {"message": "Welcome, Admin! You have access to this dashboard."}
