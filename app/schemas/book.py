from typing import Annotated, Optional

from pydantic import BaseModel, field_validator, ValidationError
from fastapi import Form, HTTPException

from app.core.database import SessionLocal
from app.models.user import User


class BookResponse(BaseModel):
    id: int
    title: str
    book_image: str
    user_id: int
    price: float
    is_available: bool
    share: bool
    
    model_config = {
        "from_attributes": True
    }
   
    
class BookCreate(BaseModel):
    title: str
    price: float
    is_available: bool
    share: bool

    
    @classmethod
    def as_form(
        cls,
        title: Annotated[str, Form(min_length=3, max_length=128)],
        price: Annotated[float, Form(gt=0)],
        is_available: Annotated[bool, Form()],
        share: Annotated[bool, Form()],
    ):
        return cls(
            title=title,
            price=price,
            is_available=is_available,
            share=share   
        )
 
    
    
class BookUpdate(BaseModel):
    title: Optional[str] = None
    user_id: Optional[int] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    share: Optional[bool] = None

    
    @classmethod
    def as_form(
        cls,
        title: Annotated[Optional[str], Form(min_length=3, max_length=128)] = None,
        user_id: Annotated[Optional[int], Form(gt=0)] = None,
        price: Annotated[Optional[float], Form(gt=0)] = None,
        is_available: Annotated[Optional[bool], Form()] = None,
        share: Annotated[Optional[bool], Form()] = None,
    ):
        return cls(
            title=title,
            user_id=user_id,
            price=price,
            is_available=is_available,
            share=share   
        )
    
    
    
    