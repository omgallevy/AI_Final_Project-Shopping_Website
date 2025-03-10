from typing import Optional, List

from pydantic import BaseModel

from model.order_item import OrderItem


class OrderRequest(BaseModel):
    shipping_address: Optional[str] = None
    items: List[OrderItem]
