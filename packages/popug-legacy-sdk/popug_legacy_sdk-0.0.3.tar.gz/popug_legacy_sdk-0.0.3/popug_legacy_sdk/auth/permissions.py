from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes

from popug_legacy_sdk.auth.token import verify_token
from popug_legacy_sdk.schemas import TokenData


def check_permissions(
    security_scopes: SecurityScopes,
    token_data: TokenData = Depends(verify_token),
):
    token_scopes = token_data.role
    if token_scopes not in security_scopes.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
        )


def check_update_user_permissions(
    security_scopes: SecurityScopes,
    user_id: int,
    token_data: TokenData = Depends(verify_token),
):
    if token_data.role in security_scopes.scopes:
        if token_data.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't update this user",
            )
