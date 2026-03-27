from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, DeclarativeBase, sessionmaker, Session

from .config import settings

url = URL.create(
    drivername='postgresql+psycopg2',
    username=settings.db_name,
    password=settings.db_user,
    host=settings.db_pass,
    port=settings.db_host,
    database=settings.db_port,
)
engine = create_engine(url=url)
Base: DeclarativeBase = declarative_base()
sessionmaker: Session = sessionmaker()