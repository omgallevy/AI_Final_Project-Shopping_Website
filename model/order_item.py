from typing import Optional

from pydantic import BaseModel


class OrderItem(BaseModel):
    order_id: Optional[int]
    item_id: int
    quantity: int

