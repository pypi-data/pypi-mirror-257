from datetime import datetime, timedelta
from enum import Enum

import jwt
from pydantic import BaseModel, EmailStr

from popug_legacy_sdk.config.settings import settings


class UserRoles(Enum):
    CUSTOMER = "CUSTOMER"
    MARKET = "MARKET"
    COURIER = "COURIER"
    ADMIN = "ADMIN"


class Pagination(BaseModel):
    page_size: int = 25
    page: int = 1
    count: int = 0


class TokenData(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRoles = UserRoles.CUSTOMER.value

    class Config:
        use_enum_values = True

    def generate_token(self, expires_delta: int) -> str:
        encode_data = self.dict()
        encode_data["exp"] = datetime.utcnow() + timedelta(
            minutes=expires_delta
        )

        token: str = jwt.encode(  # type: ignore
            encode_data,
            settings.auth.secret_key,
            algorithm=settings.auth.algorithm,
        )

        return token
