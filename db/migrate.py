from config.database import engine
from config.database import Base

from models.user import User
from models.adventure import Adventure

def migrate():
    Base.metadata.create_all(bind=engine)