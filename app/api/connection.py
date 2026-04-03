from typing import Annotated, List

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..core.dependencies import get_db
from ..models.connection import ConnectionClient, Message
from .deps import get_currnet_user
from ..models.user import User
from ..schemas.connection import ConntectionMessageSchemas
from ..models.book import Book
from ..models.user import User
from ..models.swap import BuyRequest
from ..core.security import generate_tokens

router = APIRouter()


@router.get('/')
def get_user_connections(
    user: Annotated[User, Depends(get_currnet_user)],
    db: Annotated[Session, Depends(get_db)],
):
    connections = db.query(ConnectionClient).filter(
        (ConnectionClient.buy_user_id == user.id) | (ConnectionClient.client_user_id == user.id)
    ).all()
    
    return connections


@router.get('/{connection_id}/')
def get_connection(
    connection_id: int, 
    db: Annotated[Session, Depends(get_db)], 
    user: Annotated[User, Depends(get_currnet_user)]
):
    buy_r = db.query(BuyRequest).filter(BuyRequest.id==connection_id).first()
    
    if not buy_r:
        raise HTTPException(detail="Buyurtma topilmadi", status_code=404)
    
    if user.id != buy_r.book.id:
        raise HTTPException(detail="Notoggri Amal", status_code=400)
    

    format_js = [{v.book.title: v.client_user.first_name} for v in buy_r.conntections]
    
    return format_js

# print(generate_tokens(1))
@router.post('/{buy_request_id}/')
def send_message(
    buy_request_id: int, 
    db: Annotated[Session, Depends(get_db)],
    data: Annotated[ConntectionMessageSchemas, Body()], 
    user: Annotated[User, Depends(get_currnet_user)]
):
    buy_r = db.query(BuyRequest).filter(BuyRequest.id==buy_request_id).first()
    book = db.query(Book).filter(Book.id==buy_r.book_id).first()
    
    if not buy_r:
        raise HTTPException(detail="Bunday Buyurtma Mavjud emas", status_code=404)
    
    
    conn = db.query(ConnectionClient).filter(or_(ConnectionClient.buy_user_id==user.id, ConnectionClient.client_user_id==user.id)).first()
    if not conn:
        conn = ConnectionClient(
            buy_user_id=user.id,
            client_user_id=buy_r.user_id,
            book_id=book.id,
            book_request_id=buy_r.id,
        )
        
        db.add(conn)
        db.flush()
    
    mess = Message(
        conntection_id=conn.id,
        user_id=user.id,
        message=data.message,   
    )
    
    db.add(mess)
    db.commit()
    db.refresh(mess)
    
    fm_js = {conn.book.title: [
        {user.first_name: data.message}
    ]}
    
    return fm_js


@router.get('/{connection_id}/messages/')
def get_messages(
    connection_id: int, 
    db: Annotated[Session, Depends(get_db)], 
    user: Annotated[User, Depends(get_currnet_user)]
):
    conn = db.query(ConnectionClient).filter(ConnectionClient.id==connection_id).first()
    
    if not conn:
        raise HTTPException(detail="Boglanish Topilmadi.", status_code=404)
    
    if conn.buy_user_id != user.id and conn.client_user_id != user.id:
        raise HTTPException(detail="Notogri Amal", status_code=400)
    
    fm_js = {conn.book.title: [
        {v.user.first_name: v.message} for v in conn.message
    ]}
    
    return fm_js 


