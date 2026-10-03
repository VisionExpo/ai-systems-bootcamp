from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.dependencies import get_item_service
from app.services import ItemService
from app.models import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

items_db : dict[int, Item] = {}
next_id = 1

@router.post("/", response_model=Item)
def create_item(
        item: ItemCreate,
        service: ItemService = Depends(get_item_service)
) -> Item:
    return service.create(item)


@router.get("/", response_model=list[Item])
def list_items():
    return list(items_db.values())

@router.get("/{item_id}", response_model=Item)
def get_item(
        item_id: int,
        service: ItemService = Depends(get_item_service)
):
    return service.get(item_id)

@router.put("/{item_id}", response_model=Item)
def update_item(
        item_id: int,
        item: ItemCreate,
        service: ItemService = Depends(get_item_service)
):
    return service.update(item_id, item)

@router.delete("/{item_id}")
def delete_item(
        item_id: int,
        service: ItemService = Depends(get_item_service)
):
    return service.delete(item_id)