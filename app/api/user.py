from typing import Annotated

from fastapi import Depends, Body, HTTPException, status
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from ..schemas.user import Login,VerifyCode
from ..core.dependencies import get_db
from ..core.security import verify_token, hash_password, verify_password
from ..models.user import User
from ..api.deps import get_currnet_user


router = APIRouter()

@router.post('/login')
async def create_user(
    user_data: Annotated[Login, Body()], 
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query()
    

@router.post('verify-otp')
async def verify_otp(
    data: Annotated[VerifyCode, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    pass


@router.get('/me')
async def get_current_user(
    user: Annotated[dict, Depends(get_currnet_user)],
):
    return user