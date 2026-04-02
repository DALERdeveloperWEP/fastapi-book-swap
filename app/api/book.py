from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from ..models.book import Book
from app.core.dependencies import get_db
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.core.security import upload_image
from app.models.user import User
from app.api.deps import get_currnet_user, check_user_isauthenticated

router = APIRouter()


@router.get('/')
async def get_books(db: Annotated[Session, Depends(get_db)]) -> List[BookResponse]:
    books = db.query(Book).filter(Book.share == True).all()
    return books


@router.post('/')
async def create_book(
    request: Request, 
    user: Annotated[User, Depends(get_currnet_user)],
    data: Annotated[BookCreate, Depends(BookCreate.as_form)],
    image_file: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)]
) -> BookResponse:
    
    user = db.query(User).filter(User.id == user.id).first()
    
    if not user:
        raise HTTPException(detail="User not found", status_code=400)
    
    image_path = await upload_image(image_file)
    
    if not image_path:
        raise HTTPException(detail="Book only accepts image files", status_code=400)
    
    new_book = Book(
        title=data.title,
        price=data.price,
        user_id=user.id,
        is_available=data.is_available,
        share=data.share,
        book_image=image_path
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get('/{book_id}')
async def get_book(
    book_id: int,
    user: Annotated[User, Depends(check_user_isauthenticated)],
    db: Annotated[Session, Depends(get_db)]
) -> BookResponse:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(detail="Book not found", status_code=404)
    
    if not book.share:
        if not user or book.user_id != user.id:
            raise HTTPException(detail="Book not found", status_code=404)
        else:
            return book
    else:
        return book
    


@router.put('/{book_id}')
async def update_book(
    book_id: int, 
    user: Annotated[User, Depends(get_currnet_user)],
    data: Annotated[BookUpdate, Depends(BookUpdate.as_form)], 
    db: Annotated[Session, Depends(get_db)],
    image_file: Annotated[UploadFile, File()] = None
) -> BookResponse:
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(detail="Book not found", status_code=404)

    if book.user_id != user.id:
        raise HTTPException(detail="You are not authorized to update this book", status_code=403)
    
    book.title = data.title if data.title else book.title
    book.price = data.price if data.price else book.price
    book.is_available = data.is_available if data.is_available else book.is_available
    book.share = data.share if data.share else book.share
    
    db.commit()
    db.refresh(book)
    return book



@router.patch('/{book_id}')
async def update_book_patch(
    book_id: int,
    user: Annotated[User, Depends(get_currnet_user)],
    data: Annotated[BookUpdate, Depends(BookUpdate.as_form)], 
    db: Annotated[Session, Depends(get_db)]
) -> BookResponse:

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(detail="Book not found", status_code=404)
    
    if book.user_id != user.id:
        raise HTTPException(detail="You are not authorized to update this book", status_code=403)
    
    book.title = data.title if data.title else book.title
    book.price = data.price if data.price else book.price
    book.is_available = data.is_available if data.is_available else book.is_available
    book.share = data.share if data.share else book.share
    
    db.commit()
    db.refresh(book)
    return book



@router.delete('/{book_id}')
async def delete_book(
    book_id: int, 
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(detail="Book not found", status_code=404)

    if book.user_id != user.id:
        raise HTTPException(detail="You are not the owner of this book", status_code=403)
    
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}