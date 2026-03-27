from typing import Annotated

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from app.api.router import router
from .core.database import Base, engine
from .core.dependencies import get_db
from .models.user import User
from .models.book import Book
from .models.swap import BuyRequest

app = FastAPI()
app.include_router(router, prefix='/api')


@app.get('/')
async def Home(db: Annotated[Session, Depends(get_db)]):
    print(db.query(User).all())
    return {"messange": "Hello World"}


Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)