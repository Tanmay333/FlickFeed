from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from redis_config import redis_client  # Import Redis connection

security = HTTPBearer()

def get_current_token(token: str = Security(security)):
    """
    Extract token and check if it is blacklisted
    """
    token = token.credentials  # Extract token from header

    # Check if token is blacklisted
    if redis_client.exists(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return token 