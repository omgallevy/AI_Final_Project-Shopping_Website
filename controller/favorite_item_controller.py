
from typing import List

from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from model.favorite_item_request import FavoriteItemRequest
from model.favorite_item_response import FavoriteItemResponse
from service import favorite_item_service, auth_service

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/{favorite_item_id}", response_model=FavoriteItemResponse)
async def get_favorite_item(favorite_item_id: int):
    favorite_item = await favorite_item_service.get_by_id(favorite_item_id)
    if not favorite_item:
        raise HTTPException(status_code=404, detail="Favorite item not found")
    return favorite_item


@router.get("/users/{user_id}/favorites", response_model=List[FavoriteItemResponse])
async def get_favorite_items_by_user(token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    favorite_items = await favorite_item_service.get_favorite_items_by_user_id(user.id)
    return favorite_items


@router.get("/users/username/{username}/favorites", response_model=List[FavoriteItemResponse])
async def get_favorite_items_by_username(username: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if user.username != username:
        raise HTTPException(status_code=403, detail="Unauthorized access to favorites")
    favorite_items = await favorite_item_service.get_favorite_items_by_user_username(user.username)
    return favorite_items


@router.get("/users/{user_id}/items/{item_id}", response_model=FavoriteItemResponse)
async def get_favorite_item_by_user_and_item(item_id: int, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    favorite_item = await favorite_item_service.get_by_user_id_and_item_id(user.id, item_id)
    if not favorite_item:
        raise HTTPException(status_code=404, detail="Favorite item not found")
    return favorite_item


@router.get("/{item_name}", response_model=FavoriteItemResponse)
async def get_favorite_item_by_name(item_name: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    favorite_item = await favorite_item_service.get_favorite_item_by_name(user.id, item_name)
    if not favorite_item:
        raise HTTPException(status_code=404, detail="Favorite item not found")
    return favorite_item


@router.post("/items_name")
async def create_favorite_item_by_name(item_name: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    await favorite_item_service.create_favorite_item_by_name(user.id, item_name)


@router.post("/")
async def create_favorite_item(favorite_item: FavoriteItemRequest):
    return await favorite_item_service.create_favorite_item(favorite_item)


@router.delete("/delete/{item_name}")
async def delete_favorite_item_by_name(item_name: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    try:
        await favorite_item_service.delete_by_name(user.id, item_name)
        return {"message": "Favorite item removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("delete/{favorite_item_id}", status_code=204)
async def delete_by_id(favorite_item_id: int):
    try:
        await favorite_item_service.delete_by_id(favorite_item_id)
        return {"message": "Favorite item removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
