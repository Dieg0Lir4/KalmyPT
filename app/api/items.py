from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemPaginated

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=ItemPaginated)
def get_items(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    service = ItemService(db)
    return service.get_all(page, size)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return ItemService(db).get_by_id(item_id)

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return ItemService(db).create(item)

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    return ItemService(db).update(item_id, item)

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    ItemService(db).delete(item_id)