from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    book_image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship('User', back_populates='books')