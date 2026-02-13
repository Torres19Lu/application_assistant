from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GuideBase(BaseModel):
    title: str
    category: str
    subcategory: Optional[str] = ""
    content: str
    summary: Optional[str] = ""
    cover_image: Optional[str] = ""
    is_pinned: Optional[int] = 0

class GuideCreate(GuideBase):
    pass

class GuideUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    is_pinned: Optional[int] = None

class GuideResponse(GuideBase):
    id: int
    views: int
    likes: int
    author_id: int
    author_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
