from typing import Annotated, Optional
from pydantic import BaseModel, Field

class BuyCreate(BaseModel):
    book_id: Annotated[int, Field(gt=0)]
    total_books: Annotated[int, Field(gt=0)]
    delivery_method: Annotated[str, Field(examples=['pickup'])]
    
    

class BuyResponse(BaseModel):
    id: int
    book_id:int 
    total_books:int 
    delivery_method:str 
    status: str
    
    model_config = {
        "from_attributes": True
    }
    
    

class BuyUpdate(BaseModel):
    total_books: Annotated[Optional[int], Field(gt=0)] = None
    delivery_method: Annotated[Optional[str], Field()] = None
    status: Annotated[Optional[str], Field()] = None
    
    
    
    
"""
delivery_method ichida quyidagi qiymatlar bo‘lishi mumkin:

"pickup" → user o‘zi kelib olib ketadi
"courier" → kuryer orqali yetkaziladi
"post" → pochta orqali yuboriladi
"delivery" → umumiy yetkazib berish
"""