from typing import Optional, List, Union, Dict

from fastapi import HTTPException
from starlette import status

from model.order import Order
from model.order_item import OrderItem
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository import order_repository, order_items_repository
from service import item_service


async def get_order_by_id(order_id: int) -> Optional[OrderResponse]:
    return await order_repository.get_order_by_id(order_id)


async def get_all_orders_by_user(user_id: int) -> Optional[List[Order]]:
    return await order_repository.get_all_orders_by_user(user_id)


async def get_order_by_id_and_user(user_id: int, order_id: int) -> Optional[OrderResponse]:
    order = await order_repository.get_order_by_id(order_id)
    if order and order.user_id == user_id:
        return order
    return None


async def get_all_orders_by_username_service(username: str) -> Optional[List[dict]]:
    orders = await order_repository.get_all_orders_by_username(username)
    if not orders:
        return []
    return orders


async def get_order_by_id_and_username_service(username: str, order_id: int) -> OrderResponse:
    order = await order_repository.get_order_by_id_and_username(username, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order


async def create_order(order: OrderRequest, user_id: int) -> int:
    temp_order = await order_repository.get_orders_by_status(user_id, OrderStatus.TEMP)
    if not temp_order:
        order_id = await order_repository.create_order(order, user_id)
    else:
        order_id = temp_order[0].id

    for item in order.items:
        item_in_stock = await item_service.get_item_by_id(item.item_id)
        if item.quantity > item_in_stock.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There are only {item_in_stock.stock} units in stock. Please adjust your order."
            )
        item_in_order = await order_items_repository.get_item_in_order(order_id,item.item_id)
        if item_in_order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chosen item is already in order"
            )

        order_item = OrderItem(order_id=order_id, item_id=item.item_id, quantity=item.quantity)
        await order_items_repository.create_order_item(order_item)

    return order_id


async def update_order(order_id: int, order: OrderRequest):
    existing_order = await order_repository.get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if existing_order.status == OrderStatus.CLOSE:
        raise HTTPException(status_code=400, detail="Cannot modify a closed order.")
    await order_repository.update_order(order_id, order)


async def delete_by_id(order_id: int):
    order = await order_repository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if order.status == OrderStatus.CLOSE:
        raise HTTPException(status_code=400, detail="Cannot delete a closed order.")
    await order_repository.delete_by_id(order_id)


async def close_order(order_id: int, user_id: int) -> bool:
    order = await order_repository.get_order_by_id(order_id)
    if order and order.status == OrderStatus.TEMP and order.user_id == user_id:
        items_in_order = await order_repository.get_order_items_with_details(order_id)
        for item in items_in_order:
            await item_service.update_items_quantity(item['item_id'], item['quantity'])
        await order_repository.close_order(order_id)
        return True
    return False
