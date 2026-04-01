import json
from typing import Annotated

from fastapi import Depends, Body, HTTPException, status
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from ..schemas.user import Login,VerifyCode
from ..core.dependencies import get_db
from ..core.security import delete_otp, generate_tokens, verify_token, hash_password, verify_password
from ..models.user import User
from ..api.deps import get_currnet_user
from ..core.security import genegrate_otp, get_otp


router = APIRouter()

@router.post('/auth/login', responses={
    200: {"description": "OTP sent to your telegram phone number"},
    404: {"description": "User not found"}
})
async def login_user(
    user_data: Annotated[Login, Body()], 
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.phone == user_data.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    print(genegrate_otp(user_data.phone_number, login_panding=True))
        
    return {"message": "OTP sent to your telegram phone number"}


@router.post('/auth/verify-otp', responses={
    200: {"description": "OTP verified successfully, tokens generated"},
    400: {"description": "Invalid or expired OTP"},
    404: {"description": "User not found"}
})
async def verify_otp(
    data: Annotated[VerifyCode, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    user_phone = data.phone_number
    
    user = db.query(User).filter(User.phone == user_phone).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    
    
    otp = get_otp(user_phone)
    user_otp = data.verify_code
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
        
    user_dict_otp = json.loads(get_otp(user_phone))
    
    if user_dict_otp['OTP'] != str(user_otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    delete_otp(user_phone)
    
    return generate_tokens(str(user.id))

    
    

@router.get('/auth/me')
async def user_bio(
    user: Annotated[dict, Depends(get_currnet_user)],
):
    return {'message': 'This is protected route', 'user_id': user.id}