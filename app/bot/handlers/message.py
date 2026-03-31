from telegram import Update
from telegram.ext import ContextTypes

from ..services.user import check_user, save_phone_number
from app.core.database import SessionLocal
from app.models.user import User
from ..services.keyboar_text import *

async def contact_message(update: Update, contex: ContextTypes):
    session = SessionLocal()
    match check_user(update=update, session=session):
        case 'create user':
            if save_phone_number(update=update, session=session):
                await update.message.reply_text(phone_access, reply_markup=menu_keyboard)
                return
            else:
                return
            
        case 'not phone number':
            if save_phone_number(update=update, session=session):
                await update.message.reply_text(phone_access, reply_markup=menu_keyboard)
                return
            else:
                return
                      
        case 'user exist':
            await update.message.reply_text(user_start, reply_markup=menu_keyboard)
        case _:
            await update.message.reply_text(user_start, reply_markup=menu_keyboard)
            pass
        

