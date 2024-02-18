from pydantic import BaseModel


class AuthSettings(BaseModel):
    secret_key: str
    algorithm: str
    expired_token: int = 15
    expired_refresh_token: int = 600
