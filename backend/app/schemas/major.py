from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MajorBase(BaseModel):
    name: str
    name_en: Optional[str] = ""
    category: str
    subcategory: Optional[str] = ""
    university_id: int
    duration: Optional[str] = ""
    tuition: Optional[str] = ""
    ielts_requirement: Optional[str] = ""
    toefl_requirement: Optional[str] = ""
    gpa_requirement: Optional[float] = 0.0
    gre_requirement: Optional[str] = ""
    gmat_requirement: Optional[str] = ""
    description: Optional[str] = ""
    curriculum: Optional[str] = ""
    career_prospects: Optional[str] = ""
    admission_rate: Optional[float] = 0.0
    avg_gpa: Optional[float] = 0.0
    avg_ielts: Optional[float] = 0.0
    total_admitted: Optional[int] = 0

class MajorCreate(MajorBase):
    pass

class MajorUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    university_id: Optional[int] = None
    duration: Optional[str] = None
    tuition: Optional[str] = None
    ielts_requirement: Optional[str] = None
    toefl_requirement: Optional[str] = None
    gpa_requirement: Optional[float] = None
    gre_requirement: Optional[str] = None
    gmat_requirement: Optional[str] = None
    description: Optional[str] = None
    curriculum: Optional[str] = None
    career_prospects: Optional[str] = None
    admission_rate: Optional[float] = None
    avg_gpa: Optional[float] = None
    avg_ielts: Optional[float] = None
    total_admitted: Optional[int] = None

class MajorResponse(MajorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    university_name: Optional[str] = None
    university_logo: Optional[str] = None
    country: Optional[str] = None
    
    class Config:
        from_attributes = True
