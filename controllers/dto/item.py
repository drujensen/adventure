from typing import Optional
from pydantic import BaseModel

class ItemData(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
