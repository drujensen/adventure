from fastapi import FastAPI
from config.settings import settings
from controllers.home import home_router
from controllers.items import items_router

app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION)

app.include_router(home_router)
app.include_router(items_router)
