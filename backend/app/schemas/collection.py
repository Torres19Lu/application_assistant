from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class CollectionBase(BaseModel):
    collection_type: str
    target_id: int

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id: int
    user_id: int
    created_at: datetime
    target: Optional[Any] = None
    
    class Config:
        from_attributes = True
