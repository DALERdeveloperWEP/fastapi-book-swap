import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=24), nullable=True)
    last_name = Column(String(length=24), nullable=True)
    telegram_id = Column(String(11), nullable=False, unique=True)
    phone = Column(String(15), nullable=True, unique=True)
    email = Column(String(255), nullable=True, index=True, unique=True)
    password = Column(String(255))
    avatar = Column(String, nullable=True)
    role = Column(String, default='user')
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    books = relationship('Book', back_populates='user')
    buyrequests = relationship('BuyRequest', back_populates='user')

