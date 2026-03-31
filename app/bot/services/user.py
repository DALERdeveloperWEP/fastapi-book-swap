from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User

def check_user(update, session):
    
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
        
        # await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return 'create user'
    
    elif not user.phone:
        # await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return 'not phone number'
    else:
        # await update.message.reply_text(first_start, reply_markup=auth_keyboard)
        return 'user exist'
    


def save_phone_number(update, session):
            
    phone_number = update.message.contact.phone_number
    contact_id = update.message.contact.user_id
    telegram_id = str(update.message.from_user.id)
    
    if str(contact_id) != telegram_id:
        return False
    
    user = session.query(User).filter(User.telegram_id==telegram_id).first()
    user.phone = phone_number if phone_number.startswith('+') else f'+{phone_number}'
    session.commit()
    session.refresh(user)
    return True