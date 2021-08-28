from fastapi import APIRouter
from typing import Optional

from controllers.dto.item import Item

items_router = APIRouter(prefix="/items")

@items_router.get("/")
def read_items(q:Optional[str] = None):
    return {"q": q}

@items_router.post("/")
def create_item(item: Item):
    return {"name": item.name,"price": item.price}

@items_router.get("/{item_id}")
def read_item(item_id:int):
    return {"item_id": item_id}

@items_router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    return {"name": item.name,"price": item.price, "id": item_id}

@items_router.delete("/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id}
