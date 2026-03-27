from fastapi import FastAPI
from app.api.router import router

from .core.database import Base, engine

app = FastAPI()
# app.include_router(router, prefix='/api')


@app.get('/')
async def Home():
    return {"messange": "Hello World"}


# Base.metadata.create_all(bind=engine)