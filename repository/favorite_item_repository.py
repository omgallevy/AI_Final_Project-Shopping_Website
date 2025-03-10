from typing import Optional, List
from model.favorite_item import FavoriteItem

from repository.database import database

TABLE_FAVORITE_NAME = "favorite_item"
TABLE_ITEM_NAME = "items"


async def get_by_id(favorite_item_id: int) -> Optional[FavoriteItem]:
    query = f"""
        SELECT favorite_item.id, favorite_item.user_id, favorite_item.item_id, 
               items.name AS item_name, items.price AS item_price, items.stock AS item_stock
        FROM {TABLE_FAVORITE_NAME}
        JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
        WHERE favorite_item.id = :favorite_item_id
        """
    result = await database.fetch_one(query, values={"favorite_item_id": favorite_item_id})
    return dict(result) if result else None


async def get_favorite_items_by_user_id(user_id: int) -> Optional[list[dict]]:
    query = f"""
    SELECT favorite_item.id, favorite_item.user_id, favorite_item.item_id, 
           items.name AS item_name, items.price AS item_price, items.stock AS item_stock
    FROM {TABLE_FAVORITE_NAME}
    JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
    WHERE favorite_item.user_id = :user_id
    """
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [dict(result) for result in results] if results else None


async def get_favorites_by_username(username: str) -> List[dict]:
    user_id_query = "SELECT id FROM users WHERE username = :username"
    user_id_result = await database.fetch_one(user_id_query, values={"username": username})

    if not user_id_result:
        return []

    user_id = user_id_result["id"]

    query = f"""
        SELECT items.name AS item_name, items.price AS item_price, items.stock AS item_stock
        FROM {TABLE_FAVORITE_NAME}
        JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
        WHERE favorite_item.user_id = :user_id
    """
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [dict(result) for result in results]


async def get_by_user_id_and_item_id(user_id: int, item_id: int) -> Optional[dict]:
    query = f"""
    SELECT favorite_item.id, favorite_item.user_id, favorite_item.item_id, 
           items.name AS item_name, items.price AS item_price, items.stock AS item_stock
    FROM {TABLE_FAVORITE_NAME}
    JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
    WHERE favorite_item.user_id = :user_id AND favorite_item.item_id = :item_id
    """
    result = await database.fetch_one(query, values={"user_id": user_id, "item_id": item_id})
    return dict(result) if result else None


async def get_favorite_item_by_name(user_id, item_name):
    query = f"""
        SELECT favorite_item.id, favorite_item.user_id, favorite_item.item_id, 
               items.name AS item_name, items.price AS item_price, items.stock AS item_stock
        FROM {TABLE_FAVORITE_NAME}
        JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
        WHERE favorite_item.user_id = :user_id AND items.name = :item_name
        """
    result = await database.fetch_one(query, values={"user_id": user_id, "item_name": item_name})
    return dict(result) if result else None


async def create_favorite_item_by_name(user_id: int, item_name: str):
    item_query = f"SELECT id FROM {TABLE_ITEM_NAME} WHERE name = :item_name"
    item = await database.fetch_one(item_query, values={"item_name": item_name})
    if not item:
        raise ValueError("Item not found")

    query = f"""
            INSERT INTO {TABLE_FAVORITE_NAME} (user_id, item_id)
            VALUES (:user_id, :item_id)
            """
    await database.execute(query, values={"user_id": user_id, "item_id": item[0]})


async def create_favorite_item(favorite_item: FavoriteItem) -> int:
    query = f"""
        INSERT INTO {TABLE_FAVORITE_NAME} (user_id, item_id)
        VALUES (:user_id, :item_id)
    """
    values = {"user_id": favorite_item.user_id, "item_id": favorite_item.item_id}
    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]


async def delete_by_id(favorite_item_id: int):
    query = f"DELETE FROM {TABLE_FAVORITE_NAME} WHERE id=:favorite_item_id"
    await database.execute(query, values={"favorite_item_id": favorite_item_id})


async def delete_by_name(user_id: int, item_name: str) -> None:
    favorite_query = f"""
    SELECT favorite_item.id
    FROM {TABLE_FAVORITE_NAME}
    JOIN {TABLE_ITEM_NAME} ON favorite_item.item_id = items.id
    WHERE favorite_item.user_id = :user_id AND items.name = :item_name
    """
    favorite_item = await database.fetch_one(favorite_query, values={"user_id": user_id, "item_name": item_name})
    if not favorite_item:
        raise ValueError("Favorite item not found")

    delete_query = f"DELETE FROM {TABLE_FAVORITE_NAME} WHERE id = :favorite_item_id"
    await database.execute(delete_query, values={"favorite_item_id": favorite_item["id"]})
