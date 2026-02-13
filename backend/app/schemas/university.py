from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UniversityBase(BaseModel):
    name: str
    name_en: Optional[str] = ""
    country: str
    region: Optional[str] = ""
    qs_ranking: Optional[int] = None
    us_news_ranking: Optional[int] = None
    difficulty: Optional[str] = "medium"
    description: Optional[str] = ""
    location: Optional[str] = ""
    tuition_range: Optional[str] = ""
    logo_url: Optional[str] = ""
    website: Optional[str] = ""
    application_requirements: Optional[str] = ""

class UniversityCreate(UniversityBase):
    pass

class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    qs_ranking: Optional[int] = None
    us_news_ranking: Optional[int] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    tuition_range: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    application_requirements: Optional[str] = None

class UniversityResponse(UniversityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
