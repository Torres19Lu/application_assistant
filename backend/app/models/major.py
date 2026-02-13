from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class Major(Base):
    __tablename__ = "majors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200), default="")
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), default="")
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    duration = Column(String(50), default="")
    tuition = Column(String(100), default="")
    ielts_requirement = Column(String(20), default="")
    toefl_requirement = Column(String(20), default="")
    gpa_requirement = Column(Float, default=0.0)
    gre_requirement = Column(String(20), default="")
    gmat_requirement = Column(String(20), default="")
    description = Column(Text, default="")
    curriculum = Column(Text, default="")
    career_prospects = Column(Text, default="")
    admission_rate = Column(Float, default=0.0)
    avg_gpa = Column(Float, default=0.0)
    avg_ielts = Column(Float, default=0.0)
    total_admitted = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    university = relationship("University", back_populates="majors")
