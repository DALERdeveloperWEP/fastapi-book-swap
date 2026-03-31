from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from ..models.user import User
from ..core.security import verify_token
from ..core.dependencies import get_db


bearer = HTTPBearer()

def get_currnet_user(
    cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    decode_token = verify_token(cred.credentials)
    
    if not decode_token:
        pass
    
    print(decode_token['user_id'])
    
    return None
    