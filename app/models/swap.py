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
    # location = Column(String())
    status = Column(String(24), nullable=False, default='pending')
    
    book = relationship('Book', back_populates='buyrequests')
    user = relationship('User', back_populates='buyrequests')
    conntections = relationship("ConnectionClient", back_populates='buy_request')
    

    def __str__(self):
        return f"""{{'id': {self.id}, 'book_id': {self.book_id}, 'user_id': {self.user_id}, 'total_books': {self.total_books}, 'delivery_method': {self.delivery_method}, 'status': {self.status}}}"""
    
    def __repr__(self):
        return f"""{{'id': {self.id}, 'book_id': {self.book_id}, 'user_id': {self.user_id}, 'total_books': {self.total_books}, 'delivery_method': {self.delivery_method}, 'status': {self.status}}}"""
