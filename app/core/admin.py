from sqladmin import ModelView
from app.core.database import engine
from app.models.user import User
from app.models.book import Book


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name, User.telegram_id, User.phone]


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.price, Book.is_available, Book.share, Book.created_at, Book.updated_at]