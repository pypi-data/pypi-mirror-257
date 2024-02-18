import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from popug_legacy_sdk.config.settings import settings
from popug_legacy_sdk.schemas import TokenData

security = HTTPBearer()
security.model.description = (
    "JWT Authorization header using the Bearer scheme. "
    "Example:Authorization: {token}"
)


def verify_token(access_token: str = Depends(security)) -> TokenData:
    return decode_token(access_token.credentials)


def decode_token(token: str) -> TokenData:
    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token, settings.auth.secret_key, settings.auth.algorithm
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return TokenData(**payload)
