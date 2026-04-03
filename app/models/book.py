from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(128), nullable=False, index=True)
    book_image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    share = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship('User', back_populates='books')
    buyrequests = relationship('BuyRequest', back_populates='book')
    conntections = relationship("ConnectionClient", back_populates='book')
    
    
    def __repr__(self):
        return f'{self.title}'
    
    def __str__(self):
        return f'{self.title}'