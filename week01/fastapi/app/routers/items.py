from fastapi import APIRouter, HTTPException
from app.models import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

items_db : dict[int, Item] = {}
next_id = 1

@router.post("/", response_model=Item)
def create_item(item: ItemCreate):
    global next_id

    new_item = Item(id=next_id, **item.model_dump())
    items_db[next_id] = new_item
    next_id += 1

    return new_item

@router.get("/", response_model=list[Item])
def list_items():
    return list(items_db.values())

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    updated = Item(id=item_id, **item.model_dump())
    items_db[item_id] = updated
    return updated

@router.delete("/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": "Item deleted successfully"}

