from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # ===== 申请人基本信息 =====
    applicant_name = Column(String(100), default="匿名")
    
    # 本科院校（支持数据库内院校关联 + 自由输入）
    undergraduate_university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)
    undergraduate_university_name = Column(String(200), default="")  # 自由输入或自动填充
    undergraduate_major = Column(String(200), default="")
    graduation_year = Column(Integer, nullable=True)
    
    # ===== 学术成绩 =====
    gpa = Column(Float, nullable=True)
    gpa_scale = Column(Float, default=4.0)  # 4.0制 或 100制
    ranking = Column(String(50), default="")  # 如 "5/120"
    
    # ===== 语言成绩 =====
    # 雅思
    ielts_overall = Column(Float, nullable=True)
    ielts_listening = Column(Float, nullable=True)
    ielts_reading = Column(Float, nullable=True)
    ielts_writing = Column(Float, nullable=True)
    ielts_speaking = Column(Float, nullable=True)
    
    # 托福
    toefl_total = Column(Integer, nullable=True)
    toefl_reading = Column(Integer, nullable=True)
    toefl_listening = Column(Integer, nullable=True)
    toefl_speaking = Column(Integer, nullable=True)
    toefl_writing = Column(Integer, nullable=True)
    
    # GRE
    gre_total = Column(Integer, nullable=True)
    gre_verbal = Column(Integer, nullable=True)
    gre_quant = Column(Integer, nullable=True)
    gre_writing = Column(Float, nullable=True)
    
    # GMAT
    gmat_total = Column(Integer, nullable=True)
    
    # ===== 软背景 =====
    internship_count = Column(Integer, default=0)
    internship_experience = Column(Text, default="")  # 详细描述
    
    research_count = Column(Integer, default=0)
    research_experience = Column(Text, default="")
    
    publication_count = Column(Integer, default=0)
    publications = Column(Text, default="")
    
    work_years = Column(Float, default=0.0)
    work_experience = Column(Text, default="")
    
    extracurricular = Column(Text, default="")
    awards = Column(Text, default="")
    recommendation_strength = Column(String(20), default="medium")  # weak/medium/strong
    
    # ===== 录取结果 =====
    admitted_university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    admitted_major_id = Column(Integer, ForeignKey("majors.id"), nullable=False)
    admission_year = Column(Integer, default=2026)
    admission_semester = Column(String(20), default="秋季")  # 秋季/春季
    result = Column(String(20), default="录取")  # 录取/拒绝/候补/放弃
    scholarship = Column(String(200), default="")
    
    # ===== 元数据 =====
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_verified = Column(Integer, default=0)  # 管理员审核
    remarks = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    undergraduate_university = relationship("University", foreign_keys=[undergraduate_university_id])
    admitted_university = relationship("University", foreign_keys=[admitted_university_id])
    admitted_major = relationship("Major", foreign_keys=[admitted_major_id])
    submitter = relationship("User", foreign_keys=[submitter_id])
