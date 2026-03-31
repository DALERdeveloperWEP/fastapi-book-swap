from time import time

import jwt
from passlib.hash import bcrypt

from .config import settings


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