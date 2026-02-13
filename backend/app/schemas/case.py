from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CaseBase(BaseModel):
    applicant_name: Optional[str] = "匿名"
    
    # 本科背景
    undergraduate_university_id: Optional[int] = None
    undergraduate_university_name: Optional[str] = ""
    undergraduate_major: Optional[str] = ""
    graduation_year: Optional[int] = None
    
    # 成绩
    gpa: Optional[float] = None
    gpa_scale: Optional[float] = 4.0
    ranking: Optional[str] = ""
    
    # 雅思
    ielts_overall: Optional[float] = None
    ielts_listening: Optional[float] = None
    ielts_reading: Optional[float] = None
    ielts_writing: Optional[float] = None
    ielts_speaking: Optional[float] = None
    
    # 托福
    toefl_total: Optional[int] = None
    toefl_reading: Optional[int] = None
    toefl_listening: Optional[int] = None
    toefl_speaking: Optional[int] = None
    toefl_writing: Optional[int] = None
    
    # GRE
    gre_total: Optional[int] = None
    gre_verbal: Optional[int] = None
    gre_quant: Optional[int] = None
    gre_writing: Optional[float] = None
    
    # GMAT
    gmat_total: Optional[int] = None
    
    # 软背景
    internship_count: Optional[int] = 0
    internship_experience: Optional[str] = ""
    research_count: Optional[int] = 0
    research_experience: Optional[str] = ""
    publication_count: Optional[int] = 0
    publications: Optional[str] = ""
    work_years: Optional[float] = 0.0
    work_experience: Optional[str] = ""
    extracurricular: Optional[str] = ""
    awards: Optional[str] = ""
    recommendation_strength: Optional[str] = "medium"
    
    # 录取结果
    admitted_university_id: int
    admitted_major_id: int
    admission_year: Optional[int] = 2026
    admission_semester: Optional[str] = "秋季"
    result: Optional[str] = "录取"
    scholarship: Optional[str] = ""
    
    remarks: Optional[str] = ""

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    applicant_name: Optional[str] = None
    undergraduate_university_id: Optional[int] = None
    undergraduate_university_name: Optional[str] = None
    undergraduate_major: Optional[str] = None
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None
    gpa_scale: Optional[float] = None
    ranking: Optional[str] = None
    ielts_overall: Optional[float] = None
    ielts_listening: Optional[float] = None
    ielts_reading: Optional[float] = None
    ielts_writing: Optional[float] = None
    ielts_speaking: Optional[float] = None
    toefl_total: Optional[int] = None
    toefl_reading: Optional[int] = None
    toefl_listening: Optional[int] = None
    toefl_speaking: Optional[int] = None
    toefl_writing: Optional[int] = None
    gre_total: Optional[int] = None
    gre_verbal: Optional[int] = None
    gre_quant: Optional[int] = None
    gre_writing: Optional[float] = None
    gmat_total: Optional[int] = None
    internship_count: Optional[int] = None
    internship_experience: Optional[str] = None
    research_count: Optional[int] = None
    research_experience: Optional[str] = None
    publication_count: Optional[int] = None
    publications: Optional[str] = None
    work_years: Optional[float] = None
    work_experience: Optional[str] = None
    extracurricular: Optional[str] = None
    awards: Optional[str] = None
    recommendation_strength: Optional[str] = None
    admitted_university_id: Optional[int] = None
    admitted_major_id: Optional[int] = None
    admission_year: Optional[int] = None
    admission_semester: Optional[str] = None
    result: Optional[str] = None
    scholarship: Optional[str] = None
    remarks: Optional[str] = None
    is_verified: Optional[int] = None

class CaseResponse(CaseBase):
    id: int
    submitter_id: Optional[int] = None
    is_verified: int = 0
    created_at: datetime
    updated_at: datetime
    # 关联信息
    undergraduate_university_display: Optional[str] = None
    admitted_university_name: Optional[str] = None
    admitted_major_name: Optional[str] = None
    admitted_country: Optional[str] = None
    submitter_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    """用户输入自己的条件，获取推荐"""
    undergraduate_university_name: Optional[str] = ""
    undergraduate_major: Optional[str] = ""
    gpa: Optional[float] = None
    gpa_scale: Optional[float] = 4.0
    ielts_overall: Optional[float] = None
    ielts_listening: Optional[float] = None
    ielts_reading: Optional[float] = None
    ielts_writing: Optional[float] = None
    ielts_speaking: Optional[float] = None
    toefl_total: Optional[int] = None
    toefl_reading: Optional[int] = None
    toefl_listening: Optional[int] = None
    toefl_speaking: Optional[int] = None
    toefl_writing: Optional[int] = None
    gre_total: Optional[int] = None
    gre_verbal: Optional[int] = None
    gre_quant: Optional[int] = None
    gre_writing: Optional[float] = None
    gmat_total: Optional[int] = None
    internship_count: Optional[int] = 0
    internship_experience: Optional[str] = ""
    research_count: Optional[int] = 0
    research_experience: Optional[str] = ""
    publication_count: Optional[int] = 0
    publications: Optional[str] = ""
    work_years: Optional[float] = 0.0
    work_experience: Optional[str] = ""
    extracurricular: Optional[str] = ""
    awards: Optional[str] = ""
    recommendation_strength: Optional[str] = "medium"

class RecommendationResult(BaseModel):
    university_id: int
    university_name: str
    major_id: int
    major_name: str
    country: str
    admission_probability: float  # 0-100%
    similar_cases_count: int
    admitted_count: int
    avg_gpa: Optional[float] = None
    avg_ielts: Optional[float] = None
    avg_toefl: Optional[float] = None
    avg_gre: Optional[float] = None
    scholarship_rate: float = 0.0
