from model.order_item import OrderItem
from repository.database import database

TABLE_NAME = "order_items"


async def create_order_item(order_item: OrderItem):
    query = f"""
        INSERT INTO {TABLE_NAME}(order_id, item_id, quantity)
        VALUES (:order_id, :item_id, :quantity)
    """
    values = {
        "order_id": order_item.order_id,
        "item_id": order_item.item_id,
        "quantity": order_item.quantity
    }

    await database.execute(query, values)


async def get_order_items_with_details(order_id: int):
    query = """
        SELECT oi.id, oi.order_id, oi.item_id, oi.quantity, i.name, i.price
        FROM order_items oi
        JOIN items i ON oi.item_id = i.id
        WHERE oi.order_id = :order_id
    """
    return await database.fetch_all(query, values={"order_id": order_id})


async def delete_order_item(order_item_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id = :order_item_id"
    await database.execute(query, values={"order_item_id": order_item_id})


async def get_item_in_order(order_id: int, item_id: int):
    query = f" SELECT * FROM {TABLE_NAME} WHERE order_id = :order_id AND item_id = :item_id"
    values= {"order_id": order_id,"item_id": item_id}
    item = await database.fetch_one(query,values)

    if item:
        return item
    else:
        return None
