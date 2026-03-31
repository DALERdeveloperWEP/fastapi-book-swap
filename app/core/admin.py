from sqladmin import ModelView
from app.core.database import engine
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id, User.phone]


