from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from model.order_item import OrderItem
from model.order_status import OrderStatus


class Order(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    shipping_address: str
    total_price: float
    items: Optional[List[OrderItem]] = None
    status: OrderStatus
