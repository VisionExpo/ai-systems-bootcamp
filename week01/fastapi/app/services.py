from app.models import Item, ItemCreate
from app.exceptions import ItemNotFoundError

class ItemService:
    def __init__(self):
        self.items_db: dict[int, Item] = {}
        self.next_id: int = 1


    def create(self, item: ItemCreate) -> Item:
        new_item = Item(
            id=self.next_id,
            **item.model_dump()
        )

        self.items_db[self.next_id] = new_item
        self.next_id += 1
        return new_item

    def get(self, item_id: int) -> Item:
        if item_id not in self.items_db:
            raise ItemNotFoundError(f"Item {item_id} not found")

        return self.items_db[item_id]

    def update(self, item_id: int, item: ItemCreate) -> Item:
        if item_id not in self.items_db:
            raise ItemNotFoundError(f"Item {item_id} not found")

        updated = Item(id=item_id, **item.model_dump())
        self.items_db[item_id] = updated

        return updated

    def delete(self, item_id: int) -> dict:
        if item_id not in self.items_db:
            raise ItemNotFoundError(f"Item {item_id} not found")

        del self.items_db[item_id]

        return {"message": "Item deleted successfully"}