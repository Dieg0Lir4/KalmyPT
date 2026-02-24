from pydantic import BaseModel, ConfigDict, Field
from typing import List

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    price: float = Field(..., gt=0)
    available: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ItemPaginated(BaseModel):
    items: List[ItemResponse]
    total: int
    page: int
    size: int