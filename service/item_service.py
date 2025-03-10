from typing import Optional, List

from model.item import ItemDetails
from repository import item_repository


async def get_item_by_id(item_id: int) -> Optional[ItemDetails]:
    return await item_repository.get_item_by_id(item_id)


async def get_all_items() -> List[ItemDetails]:
    return await item_repository.get_all_items()


async def get_items_by_stock(stock: int) -> List[ItemDetails]:
    return await item_repository.get_items_by_stock(stock)


async def get_items_stock_greater_than(stock: int) -> List[ItemDetails]:
    return await item_repository.get_items_stock_greater_than(stock)


async def get_items_stock_less_than(stock: int) -> List[ItemDetails]:
    return await item_repository.get_items_stock_less_than(stock)


async def get_items_by_name(keyword: str) -> List[ItemDetails]:
    return await item_repository.get_items_by_name(keyword)


async def update_items_quantity(item_id: int, quantity: int):
    await item_repository.update_items_quantity(item_id, quantity)