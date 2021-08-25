from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from config.settings import settings 

app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION)

class Item(BaseModel):
        name: str
        price: float
        is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello" : "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None): 
    return{"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    item.price = item.price * 1.0775
    return {"name": item.name,"price": item.price, "id": item_id}

