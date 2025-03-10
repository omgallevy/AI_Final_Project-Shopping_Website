from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int
    title: str
    price: int
