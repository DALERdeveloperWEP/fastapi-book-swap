from typing import Annotated

from fastapi import Depends, Body, HTTPException, status
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from ..schemas.user import Login
from ..core.dependencies import get_db

router = APIRouter()

@router.POST('/login')
async def create_user(
    user_data: Annotated[Login, Body()], 
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query()