from fastapi import HTTPException, APIRouter

from service import item_service

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/{item_id}")
async def get_item_by_id(item_id: int):
    item = await item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/")
async def get_all_items():
    return await item_service.get_all_items()


@router.get("/stock/{stock}")
async def get_items_by_stock(stock: int):
    return await item_service.get_items_by_stock(stock)


@router.get("/stock/greater_than/{stock}")
async def get_items_stock_greater_than(stock: int):
    return await item_service.get_items_stock_greater_than(stock)


@router.get("/stock/less_than/{stock}")
async def get_items_stock_less_than(stock: int):
    return await item_service.get_items_stock_less_than(stock)


@router.get("/name/{keyword}")
async def get_items_by_name(keyword: str):
    return await item_service.get_items_by_name(keyword)
