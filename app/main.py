from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
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
from .core.admin import MessageAdmin, UserAdmin, BookAdmin, BuyReuqeustAdmin, ConnectionClientAdmin
    
app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def custom_logger(request: Request, call_next):
    # 🔹 vaqt
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔹 user (agar yo‘q bo‘lsa unknown)
    user = getattr(request.state, "user", None)
    username = user.username if user else "unknown"
    first_name = user.first_name if user else "unknown"

    # 🔹 request info
    method = request.method
    path = request.url.path

    # 🔹 response olish
    response = await call_next(request)

    status_code = response.status_code

    # 🔹 print (log)
    print(f"{username} | {method} {path} | {now} | {status_code}")

    return response


@app.get('/')
async def Home(reqeuest: Request, db: Annotated[Session, Depends(get_db)]):
    print(db.query(User).all())
    return {"message": "Hello World"}

@app.post('/telegram/webhook', include_in_schema=False)
async def Telegram(request: Request):
    data = await request.json()
    
    bot = app.state.bot
    
    update = Update.de_json(data, bot.bot)
    await bot.process_update(update)
    
    return {"ok": True}



admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(BookAdmin)
admin.add_view(BuyReuqeustAdmin)
admin.add_view(ConnectionClientAdmin)
admin.add_view(MessageAdmin)

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)