from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from config.settings import settings

engine = create_engine(
     settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()