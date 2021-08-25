from fastapi import FastAPI
from config.settings import settings
from routers.home import home_router
from models.item import Item
from typing import Optional

app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION)

app.include_router(home_router)

@app.get("/items/{item_id}")
def read_item(item_id:int, q:Optional[str] = None):
    return{"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    item.price = item.price * 1.0775
    return {"name": item.name,"price": item.price, "id": item_id}
