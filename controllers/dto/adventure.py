from typing import Optional
from pydantic import BaseModel

from controllers.dto.utils import as_form

@as_form
class AdventureData(BaseModel):
    title: str
    description: str
    draft: Optional[bool] = None
