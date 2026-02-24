from sqlalchemy.orm import Session
from app.repositories.item_respository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from fastapi import HTTPException

class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def get_all(self, page: int, size: int):
        items, total = self.repository.get_all(page, size)
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size
        }
    
    def get_by_id(self, item_id: int):
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    
    def create(self, item: ItemCreate):
        return self.repository.create(item)
    
    def update(self, item_id: int, item: ItemUpdate):
        db_item = self.repository.get_by_id(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return self.repository.update(item_id, item)
    
    def delete(self, item_id: int):
        db_item = self.repository.get_by_id(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        self.repository.delete(item_id)