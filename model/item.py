from typing import Optional

from pydantic import BaseModel


class ItemDetails(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    stock: int
