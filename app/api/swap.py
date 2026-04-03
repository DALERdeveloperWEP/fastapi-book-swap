from typing import Annotated, List

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..schemas.buy import BuyResponse, BuyCreate, BuyUpdate
from .deps import get_currnet_user
from ..models.user import User
from ..models.book import Book
from ..models.swap import BuyRequest
from app.core.dependencies import get_db
from ..core.security import generate_tokens

router = APIRouter()

@router.get('/buys')
async def get_user_buys_buys(
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)],
) -> List[BuyResponse]:
    user_buys = db.query(BuyRequest).filter(BuyRequest.user_id==user.id).all()

    return user_buys


@router.get('/sells')
async def get_user_book_sells(
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)],
) -> List[BuyResponse]:
    sells_book = db.query(BuyRequest).join(Book, BuyRequest.book_id == Book.id).filter(Book.user_id == user.id).all()
    
    return sells_book

# print(generate_tokens(1))
@router.post('/buys')
async def book_buys(
    data: Annotated[BuyCreate, Body()],
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)],
) -> BuyResponse:
    book = db.query(Book).filter(Book.id==data.book_id).first()

    if not book:
        raise HTTPException(detail="Book not found", status_code=404)
    
    if book.user_id == user.id:
        raise HTTPException(detail="Siz O'zingiz Qoshgan Kitobni Sotib ololmaysiz", status_code=400)
    
    if data.delivery_method not in ['pickup','post']:
        raise HTTPException(detail='Iltimos (pickup, post) shulardan biror tasini tanlab yuboring', status_code=400)
    
    buy_re = db.query(BuyRequest).filter(BuyRequest.user_id==user.id).first()
    
    if buy_re:
        raise HTTPException(detail="Siz Bu Kitobni Sotib Olgansiz", status_code=400)
    
    book_buy = BuyRequest(
        book_id=data.book_id,
        user_id=user.id,
        total_books=data.total_books,
        delivery_method=data.delivery_method,
    )
    
    db.add(book_buy)
    db.commit()
    db.refresh(book_buy)
    
    return book_buy
    
    
@router.put('/buys/{buy_id}/')
async def update_buy(
    buy_id: int,
    data: Annotated[BuyUpdate, Body()],
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)]
) -> BuyResponse :
    buy = db.query(BuyRequest).filter(BuyRequest.id==buy_id).first()
    book = db.query(Book).filter(Book.id==buy.book_id).filter()
    
    if not buy:
        raise HTTPException(detail='Bunday Sotilgan Kitob Mavjud emas', status_code=404)
    
    if book.user_id == user.id:
        raise HTTPException(detail="Siz O'zingiz Qoshgan Kitobni O'zgartira ololmaysiz", status_code=400)
    
    if data.delivery_method not in ['pickup','post']:
        raise HTTPException(detail='Iltimos (pickup, post) shulardan biror tasini tanlab yuboring', status_code=400)
    
    if data.status not in ['pending', 'cancel']:
        raise HTTPException(detail='Iltimos (, cancel) shulardan biror tasini tanlab yuboring', status_code=400)
    
    buy.status = data.status if data.status else buy.status
    buy.total_books = data.total_books if data.total_books else buy.total_books
    buy.delivery_method = data.delivery_method if data.delivery_method else buy.delivery_method
    
    db.commit()
    db.refresh(buy)
    
    return buy

