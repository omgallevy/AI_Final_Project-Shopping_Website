from typing import Optional

from pydantic import BaseModel


class FavoriteItemResponse(BaseModel):
    item_name: str
    item_price: float
    item_stock: int
