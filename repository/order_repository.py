from typing import Optional, List
from model.order import Order
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository.database import database
from repository.order_items_repository import get_order_items_with_details

TABLE_NAME = "orders"


async def get_order_by_id(order_id: int) -> Optional[Order]:
    query = """
        SELECT o.id, o.order_date, o.shipping_address, o.total_price, o.status, o.user_id,
               oi.item_id, oi.quantity
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.id = :order_id
    """
    result = await database.fetch_one(query, values={"order_id": order_id})
    if result:
        return Order(**result)
    else:
        return None


async def get_all_orders_by_user(user_id: int) -> Optional[List[Order]]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id = :user_id"
    results = await database.fetch_all(query, values={"user_id": user_id})
    if results:
        return [Order(**result) for result in results]
    else:
        return None


async def get_all_orders_by_username(username: str) -> Optional[List[dict]]:
    query = """
        SELECT orders.id, orders.user_id, orders.order_date, orders.shipping_address, 
               orders.total_price, orders.status, users.username
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE users.username = :username
    """
    results = await database.fetch_all(query, values={"username": username})

    orders = []

    if results:
        for result in results:
            try:
                order_dict = dict(result)
                order_items = await get_order_items_with_details(result["id"])
                items_list = []
                for item in order_items:
                    items_list.append({
                        "item_id": item["item_id"],
                        "quantity": item["quantity"],
                        "title": item["name"],
                        "price": float(item["price"])
                    })

                order_dict["items"] = items_list
                order_dict["order_date"] = str(order_dict["order_date"])
                orders.append(order_dict)


            except Exception as e:
                print(f"⚠️ Error creating order information: {e}")
    print(orders)
    return orders


async def get_order_by_id_and_username(username: str, order_id: int) -> Optional[OrderResponse]:
    query = f"""
        SELECT orders.*, users.username
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE users.username = :username AND orders.id = :order_id
    """
    result = await database.fetch_one(query, values={"username": username, "order_id": order_id})
    return OrderResponse(**dict(result)) if result else None


async def get_orders_by_status(user_id: int, status: OrderStatus) -> Optional[List[Order]]:
    query = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE user_id = :user_id AND status = :status
    """
    results = await database.fetch_all(query, values={"user_id": user_id, "status": status.value})
    return [Order(**result) for result in results]


async def create_order(order: OrderRequest, user_id: int) -> int:
    query = """
        INSERT INTO orders (user_id, shipping_address, total_price, status)
        VALUES (:user_id, :shipping_address, :total_price, :status)
    """
    values = {
        "user_id": user_id,
        "shipping_address": order.shipping_address,
        "total_price": order.total_price,
        "status": "TEMP"
    }
    await database.execute(query, values)
    return await database.fetch_val("SELECT LAST_INSERT_ID()")


async def update_order(order_id: int, order: OrderRequest):
    query = f"""
    UPDATE {TABLE_NAME}
    SET user_id = :user_id,
        shipping_address = :shipping_address,
        items = :items
    WHERE id = :order_id
    """
    values = {
        "order_id": order_id,
        "user_id": order.user_id,
        "shipping_address": order.shipping_address,
        "items": order.items
    }
    await database.execute(query, values)


async def close_order(order_id: int):
    query = f"""
    UPDATE {TABLE_NAME}
    SET status = :status
    WHERE id = :order_id
    """
    await database.execute(query, values={"order_id": order_id, "status": OrderStatus.CLOSE.value})


async def delete_by_id(order_id: int):
    query = f"DELETE FROM order_items WHERE order_id =  :order_id"
    await database.execute(query, values={"order_id": order_id})
    query = f"DELETE FROM {TABLE_NAME} WHERE id =  :order_id"
    await database.execute(query, values={"order_id": order_id})



