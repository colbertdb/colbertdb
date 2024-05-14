import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Configuration
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Token store
NO_AUTH = os.getenv("NO_AUTH")
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "token")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify the token."""
    if NO_AUTH:
        return 'OK'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        api_token: str = payload.get("api_token")
        if api_token is None or api_token != API_AUTH_TOKEN:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    return 'OK'

