from config.database import engine
from config.database import Base


def migrate():
    Base.metadata.create_all(bind=engine)
