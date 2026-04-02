import json

from telegram import Update
from telegram.ext import ContextTypes

from ..services.user import check_user, save_phone_number
from app.core.database import SessionLocal
from app.models.user import User
from ..services.keyboar_text import *
from app.core.security import genegrate_otp, get_otp

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
        


async def otp_message(update: Update, context: ContextTypes):
    session = SessionLocal()
    match check_user(update=update, session=session):
        case 'create user':
            await update.message.reply_text(phone_reqeaired, reply_markup=auth_keyboard)
            return
        case 'not phone number':
            await update.message.reply_text(phone_reqeaired, reply_markup=auth_keyboard)
            return
        case 'user exist':
            user = session.query(User).filter(User.telegram_id==str(update.message.from_user.id)).first()
            get_user_otp = get_otp(user.phone)
            # if type(get_otp(user.phone)==dict):
            #     print('ha')
            match get_user_otp:
                case None:
                    get_user_otp = genegrate_otp(user.phone, False)
                case str() as otp:
                    try:
                        get_user_otp = json.loads(otp)['OTP']
                    except:
                        get_user_otp = otp
                    
            otp_sent = f"""{get_user_otp}"""
            await update.message.reply_text(otp_sent, reply_markup=menu_keyboard)
            return
        case _:
            await update.message.reply_text(user_start, reply_markup=menu_keyboard)
            pass