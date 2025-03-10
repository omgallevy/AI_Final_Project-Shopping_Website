from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from model.order_request import OrderRequest
from model.order_response import OrderResponse
from service import order_service, auth_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/username/{username}", response_model=Optional[List[OrderResponse]])
async def get_all_orders_by_username(username: str, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if user.username != username:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view orders for this user."
        )
    return await order_service.get_all_orders_by_username_service(username)


@router.post("/", response_model=int)
async def create_order(order: OrderRequest, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if not user:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this order."
        )
    return await order_service.create_order(order, user.id)


@router.put("/{order_id}/purchase", status_code=204)
async def update_order(order_id: int, order: OrderRequest):
    await order_service.update_order(order_id, order)


@router.delete("/delete/{order_id}", status_code=200)
async def delete_by_id(order_id: int):
    await order_service.delete_by_id(order_id)


@router.post("/close/{order_id}")
async def close_order(order_id: int, user_id: int, token: str = Depends(oauth2_bearer)):
    user = await auth_service.validate_user(token)
    if not user:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this order."
        )
    try:
        success = await order_service.close_order(order_id, user_id)
        if success:
            return True
        raise HTTPException(status_code=404, detail="Order not found or cannot be closed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
