from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from ..services.keyboar_text import *

async def start(update: Update, context: ContextTypes):
    session: Session = SessionLocal()
    
    telegram_id = str(update.effective_user.id)
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    
    user = session.query(User).filter(User.telegram_id==telegram_id).first()
    
    if not user:
        new_user = User(
            telegram_id=telegram_id,
            role='user'
        )
        if first_name:
            new_user.first_name = first_name
        if last_name:
            new_user.last_name = last_name
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return
    
    elif not user.phone:
        await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return
    else:
        await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return
    
    
