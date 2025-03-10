import json
from typing import Optional, List
from model.item import ItemDetails
from repository import cache_repository
from repository.database import database

TABLE_ITEM_NAME = "items"


async def get_item_by_id(item_id: int) -> Optional[ItemDetails]:
    query = f"SELECT * FROM {TABLE_ITEM_NAME} WHERE id = :id"
    item_data = await database.fetch_one(query, values={"id": item_id})
    return ItemDetails(**item_data) if item_data else None


async def get_all_items() -> List[ItemDetails]:
    try:
        if cache_repository.is_key_exists(TABLE_ITEM_NAME):
            all_items = cache_repository.get_cache_entity(TABLE_ITEM_NAME)
            if all_items is None or all_items == "":
                print("Cache is empty, fetching from DB")
            else:
                try:
                    all_items_data = json.loads(all_items)
                    return [ItemDetails(**item) for item in all_items_data]
                except json.JSONDecodeError as e:
                    print(f"Error decoding cached data: {e}")

        query = f"SELECT * FROM {TABLE_ITEM_NAME}"
        items_data = await database.fetch_all(query)
        items = [ItemDetails(**item) for item in items_data]
        items_list = [item.__dict__ for item in items]
        str_item_data = json.dumps(items_list)
        cache_repository.create_cache_entity(TABLE_ITEM_NAME, str_item_data)
        return items

    except Exception as e:
        print(f"Error in get_all_items: {e}")
        raise


async def get_items_by_stock(stock: int) -> List[ItemDetails]:
    query = f"SELECT * FROM {TABLE_ITEM_NAME} WHERE stock = :stock"
    items_data = await database.fetch_all(query, values={"stock": stock})
    return [ItemDetails(**item) for item in items_data]


async def get_items_stock_greater_than(stock: int) -> List[ItemDetails]:
    query = f"SELECT * FROM {TABLE_ITEM_NAME} WHERE stock > :stock"
    items_data = await database.fetch_all(query, values={"stock": stock})
    return [ItemDetails(**item) for item in items_data]


async def get_items_stock_less_than(stock: int) -> List[ItemDetails]:
    query = f"SELECT * FROM {TABLE_ITEM_NAME} WHERE stock < :stock"
    items_data = await database.fetch_all(query, values={"stock": stock})
    return [ItemDetails(**item) for item in items_data]


async def get_items_by_name(keyword: str) -> List[ItemDetails]:
    query = f"SELECT * FROM {TABLE_ITEM_NAME} WHERE name LIKE :name"
    items_data = await database.fetch_all(query, values={"name": f"%{keyword}%"})
    return [ItemDetails(**item) for item in items_data]


async def update_items_quantity(item_id: int, quantity: int):
    cache_repository.delete_cache_entity(TABLE_ITEM_NAME)
    query = f""" UPDATE {TABLE_ITEM_NAME}
    SET stock = stock - :quantity
    WHERE id = :item_id
    """
    values = {"item_id": item_id, "quantity": quantity}
    await database.execute(query, values)
