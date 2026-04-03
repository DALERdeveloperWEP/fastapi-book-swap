from sqladmin import ModelView
from app.core.database import engine
from app.models.user import User
from app.models.book import Book
from app.models.swap import BuyRequest
from app.models.connection import ConnectionClient, Message


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name, User.telegram_id, User.phone]


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.price, Book.is_available, Book.share, Book.created_at, Book.updated_at]


class BuyReuqeustAdmin(ModelView, model=BuyRequest):
    column_list = [BuyRequest.id, BuyRequest.book_id, BuyRequest.user_id, BuyRequest.total_books, BuyRequest.status, BuyRequest.delivery_method]
    

class ConnectionClientAdmin(ModelView, model=ConnectionClient):
    column_list = [ConnectionClient.buy_user, ConnectionClient.client_user, ConnectionClient.book_id, ConnectionClient.book_request_id]
    

class MessageAdmin(ModelView, model=Message):
    column_list = [Message.conntection_id, Message.user_id, Message.message]