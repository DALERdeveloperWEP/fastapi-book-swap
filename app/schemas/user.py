from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Login(BaseModel):
    phone_number: Annotated[str, Field(pattern=r"^\+998\d{9}$", examples=["+998901234567"])]
    
    # phone_number: Annotated[str, Field(min_length=13, max_length=13)]
    
    # @field_validator('phone_number')
    # def validate_phone_number(self, v):
    #     if not v.startswith("+998"):
    #         raise ValueError("Phone number must start with +998")
    #     if len(v) != 13:
    #         raise ValueError("Phone number must be 13 characters")
    #     return v
    

class VerifyCode(BaseModel):
    phone_number: Annotated[str, Field(pattern=r"^\+998\d{9}$", examples=["+998901234567"])]
    verify_code: Annotated[str, Field(max_length=6, min_length=6, examples=["Olti xonali raqam (123456)"])]
    
    