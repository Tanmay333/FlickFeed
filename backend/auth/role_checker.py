from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from backend.auth.jwt_handler import SECRET_KEY, ALGORITHM

def get_current_user_role(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Invalid token: No role found")
        return role
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(token: str = Depends(get_current_user_role)):
        if token != required_role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return token
    return role_checker
