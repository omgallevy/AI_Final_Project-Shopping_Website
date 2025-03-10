from typing import Optional, List

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from model.favorite_item_request import FavoriteItemRequest
from model.favorite_item_response import FavoriteItemResponse
from repository import favorite_item_repository
from service import auth_service


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_by_id(favorite_item_id: int) -> Optional[FavoriteItemResponse]:
    favorite_item = await favorite_item_repository.get_by_id(favorite_item_id)
    if favorite_item is not None:
        return favorite_item
    return None


async def get_favorite_items_by_user_id(user_id: int) -> Optional[List[FavoriteItemResponse]]:
    user_favorite_items = await favorite_item_repository.get_favorite_items_by_user_id(user_id)
    if user_favorite_items is not None:
        return [FavoriteItemResponse(**item) for item in user_favorite_items]
    return None


async def get_favorite_items_by_user_username(username: str) -> List[dict]:
    return await favorite_item_repository.get_favorites_by_username(username)


async def get_by_user_id_and_item_id(user_id: int, item_id: int) -> Optional[FavoriteItemResponse]:
    return await favorite_item_repository.get_by_user_id_and_item_id(user_id, item_id)


async def get_favorite_item_by_name(user_id: int, item_name: str):
    favorite_item = await favorite_item_repository.get_favorite_item_by_name(user_id, item_name)
    if not favorite_item:
        raise ValueError("Favorite item not found")
    return favorite_item


async def create_favorite_item_by_name(user_id: int, item_name: str):
    try:
        await favorite_item_repository.create_favorite_item_by_name(user_id, item_name)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def create_favorite_item(favorite_item: FavoriteItemRequest) -> Optional[int]:
    existing_item = await favorite_item_repository.get_by_user_id_and_item_id(favorite_item.user_id,
                                                                              favorite_item.item_id)
    if existing_item:
        raise HTTPException(status_code=400, detail="Item is already in favorites.")
    item_id = await favorite_item_repository.create_favorite_item(favorite_item)
    return await favorite_item_repository.get_by_id(item_id)


async def delete_by_id(favorite_item_id: int):
    existing_item = await favorite_item_repository.get_by_id(favorite_item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Favorite item not found.")
    await favorite_item_repository.delete_by_id(favorite_item_id)


async def delete_by_name( user_id: int, item_name: str):
    try:
        await favorite_item_repository.delete_by_name(user_id, item_name)
    except ValueError as e:
        raise ValueError(str(e))