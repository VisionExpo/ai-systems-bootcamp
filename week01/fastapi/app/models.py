from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class Item(ItemCreate):
    id: int