from random import randint
from .config import r

def generate_save_OTP(phone: str):
    otp = str(randint(100000, 999999))
    r.setex(phone, 120, otp)
    
def get_otp(phone: str):
    return r.get(phone)

def delete_otp(phone: str):
    r.delete(phone)