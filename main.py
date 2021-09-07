from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from middleware.method import MethodMiddleware

from config.settings import settings
from controllers.home import home_router
from controllers.adventures import adventures_router
from controllers.users import users_router
from controllers.sessions import sessions_router

from db.migrate import migrate

app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION)

app.add_middleware(MethodMiddleware)

app.include_router(home_router)
app.include_router(adventures_router)
app.include_router(users_router)
app.include_router(sessions_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

migrate()
