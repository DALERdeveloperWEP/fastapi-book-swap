from contextlib import asynccontextmanager

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from fastapi import FastAPI

from .handlers.command import start
from .handlers.message import contact_message
from ..core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    telegram_app = ApplicationBuilder().token(settings.bot_token).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.CONTACT, contact_message))

    # START
    await telegram_app.initialize()
    await telegram_app.start()

    app.state.bot = telegram_app

    yield

    # STOP
    await telegram_app.stop()
    await telegram_app.shutdown()