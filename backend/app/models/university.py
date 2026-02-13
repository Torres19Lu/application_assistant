from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200), default="")
    country = Column(String(100), nullable=False, index=True)
    region = Column(String(100), default="")
    qs_ranking = Column(Integer, nullable=True)
    us_news_ranking = Column(Integer, nullable=True)
    difficulty = Column(String(20), default="medium")
    description = Column(Text, default="")
    location = Column(String(200), default="")
    tuition_range = Column(String(100), default="")
    logo_url = Column(String(500), default="")
    website = Column(String(500), default="")
    application_requirements = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    majors = relationship("Major", back_populates="university")
