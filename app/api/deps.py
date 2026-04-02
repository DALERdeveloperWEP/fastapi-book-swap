from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from ..models.user import User
from ..core.security import verify_token
from ..core.dependencies import get_db


bearer = HTTPBearer(auto_error=False)

def get_currnet_user(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    if not cred:
        raise HTTPException(detail="Not authenticated", status_code=403)
    
    decode_token = verify_token(cred.credentials)
    
    if not decode_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id==decode_token['user_id']).first() 
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    
    return user 
    
    
def check_user_isauthenticated(
    request: Request,
    cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    if not cred:
        return False
    
    decode_token = verify_token(cred.credentials)
    
    if not decode_token:
        return False
    
    user = db.query(User).filter(User.id==decode_token['user_id']).first() 
    
    if not user:
        return False
    
    
    return True