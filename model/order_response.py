from typing import List
from pydantic import BaseModel
from model.order_item_response import OrderItemResponse


class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_date: str
    shipping_address: str
    total_price: float
    items: List[OrderItemResponse]
    status: str

