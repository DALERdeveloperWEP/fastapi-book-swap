import json
from random import randint
from time import time

import jwt
from passlib.hash import bcrypt

from .config import settings
from .config import r


SECRET = settings.secret_key
ALGO = settings.algorithm # HS256

ACCESS_EXPIRE = int(settings.access_token_expire_minutes) # minute
REFRESH_EXPIRE = int(settings.refresh_token_expire_days) # days


def generate_tokens(user_id: str) -> dict:
    now = int(time())

    access_payload = {
        "user_id": user_id,
        "exp": now + ACCESS_EXPIRE,
        "type": "access"
    }

    refresh_payload = {
        "user_id": user_id,
        "exp": now + REFRESH_EXPIRE,
        "type": "refresh"
    }

    return {
        "access_token": jwt.encode(access_payload, SECRET, algorithm=ALGO),
        "refresh_token": jwt.encode(refresh_payload, SECRET, algorithm=ALGO)
    }


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.InvalidTokenError:
        return None
    

def hash_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def genegrate_otp(phone_number: str, login_panding: bool) -> str:
    t_otp = str(randint(100000, 999999))
    otp = t_otp if not login_panding else json.dumps({"OTP": t_otp, "login_panding": True})
    r.setex(phone_number, 120, otp)  # Expire after 2 minutes
    return otp

def get_otp(phone_number: str) -> str:
    return r.get(phone_number)

def delete_otp(phone_number: str) -> None:
    if r.get(phone_number):
        r.delete(phone_number)
        return True
    else:
        return None