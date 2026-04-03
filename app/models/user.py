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

    buy_conntections = relationship("ConnectionClient", foreign_keys='ConnectionClient.buy_user_id', back_populates='buy_user')
    client_conntections = relationship("ConnectionClient", foreign_keys='ConnectionClient.client_user_id', back_populates='client_user')

    message = relationship("Message", back_populates='user')
    
    def __repr__(self):
        return f"{self.first_name} | {self.phone}"
    
    def __str__(self):
        return f"{self.first_name} | {self.phone}"
    
