from typing import Annotated

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from telegram import Update
from sqladmin import Admin

from app.api.router import router
from .core.database import Base, engine
from .core.dependencies import get_db
from .models.user import User
from .models.book import Book
from .models.swap import BuyRequest
from .bot.bot import lifespan
from .core.admin import UserAdmin

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix='/api')


@app.get('/')
async def Home(reqeuest: Request, db: Annotated[Session, Depends(get_db)]):
    print(db.query(User).all())
    return {"message": "Hello World"}

@app.post('/telegram/webhook')
async def Telegram(request: Request):
    data = await request.json()
    
    bot = app.state.bot
    
    update = Update.de_json(data, bot.bot)
    await bot.process_update(update)
    
    return {"ok": True}

admin = Admin(app, engine)
admin.add_view(UserAdmin)

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)