from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, page: int, size: int):
        offset = (page - 1) * size
        items = self.db.query(Item).offset(offset).limit(size).all()
        total = self.db.query(Item).count()
        return items, total

    def get_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def create(self, item: ItemCreate):
        db_item = Item(**item.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, item: ItemUpdate):
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        for key, value in item.model_dump().items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int):
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        self.db.delete(db_item)
        self.db.commit()