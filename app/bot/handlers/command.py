from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from ..services.keyboar_text import *
from ..services.user import check_user

async def start(update: Update, context: ContextTypes):
    session = SessionLocal()
    
    match check_user(update=update, session=session):
        case 'create user':
            await update.message.reply_text(first_start, reply_markup=auth_keyboard)
            return
        case 'not phone number':
            await update.message.reply_text(first_start, reply_markup=auth_keyboard)
            return 
        case 'user exist':
            await update.message.reply_text(user_start, reply_markup=menu_keyboard)
            return 
        case _:
            await update.message.reply_text('Xatolik yuz berdi, iltimos keyinroq urinib ko\'ring')
            return
        
