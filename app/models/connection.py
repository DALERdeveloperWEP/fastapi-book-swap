from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base



class ConnectionClient(Base):
    __tablename__ = 'connection_client'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    buy_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    client_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    book_request_id = Column(Integer, ForeignKey('buy_request.id', ondelete='CASCADE'))
    
    buy_user = relationship("User", foreign_keys=[buy_user_id], back_populates='buy_conntections')
    client_user = relationship("User", foreign_keys=[client_user_id], back_populates='client_conntections')
    
    book = relationship("Book", back_populates='conntections')
    buy_request = relationship('BuyRequest', back_populates='conntections')
    message = relationship('Message', back_populates='conntection')
    
    
    def __str__(self):
        return f'''{{"seller_id": {self.buy_user_id}, "client_id": {self.client_user_id}, "book_id": {self.book_id}}}'''
    
    def __repr__(self):
        return f'''{{"seller_id": {self.buy_user_id}, "client_id": {self.client_user_id}, "book_id": {self.book_id}}}'''
    


class Message(Base):
    __tablename__ = 'message'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conntection_id = Column(Integer, ForeignKey('connection_client.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    message = Column(String(1000), nullable=False)
    
    conntection = relationship("ConnectionClient", back_populates='message')
    user = relationship("User", back_populates='message')
    
    
    
    def __str__(self):
        return f'''{{"user_id": {self.user_id}, "connection_id": {self.conntection_id}, "message": "{self.message[:20]}"}}'''
    
    def __repr__(self):
        return f'''{{"user_id": {self.user_id}, "connection_id": {self.conntection_id}, "message": "{self.message[:20]}"}}'''