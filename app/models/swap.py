from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base

class BuyRequest(Base):
    __tablename__ = 'buy_request'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='RESTRICT'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    total_books = Column(Integer, nullable=False)
    delivery_method = Column(String(64), nullable=False)
    status = Column(String(24), nullable=False, default='pending')
    
    book = relationship('Book', back_populates='buyrequests')
    user = relationship('User', back_populates='buyrequests')
    
