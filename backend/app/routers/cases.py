from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.models.case import Case
from app.models.university import University
from app.models.major import Major
from app.models.user import User
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate, RecommendationRequest, RecommendationResult
from app.services.recommendation import generate_recommendations
from app.routers.auth import get_current_user, get_current_admin, get_optional_user

router = APIRouter(prefix="/cases", tags=["录取案例"])


def _case_to_dict(case: Case) -> dict:
    """将 Case ORM 对象转换为响应字典"""
    return {
        "id": case.id,
        "applicant_name": case.applicant_name,
        "undergraduate_university_id": case.undergraduate_university_id,
        "undergraduate_university_name": case.undergraduate_university_name,
        "undergraduate_major": case.undergraduate_major,
        "graduation_year": case.graduation_year,
        "gpa": case.gpa,
        "gpa_scale": case.gpa_scale,
        "ranking": case.ranking,
        "ielts_overall": case.ielts_overall,
        "ielts_listening": case.ielts_listening,
        "ielts_reading": case.ielts_reading,
        "ielts_writing": case.ielts_writing,
        "ielts_speaking": case.ielts_speaking,
        "toefl_total": case.toefl_total,
        "toefl_reading": case.toefl_reading,
        "toefl_listening": case.toefl_listening,
        "toefl_speaking": case.toefl_speaking,
        "toefl_writing": case.toefl_writing,
        "gre_total": case.gre_total,
        "gre_verbal": case.gre_verbal,
        "gre_quant": case.gre_quant,
        "gre_writing": case.gre_writing,
        "gmat_total": case.gmat_total,
        "internship_count": case.internship_count,
        "internship_experience": case.internship_experience,
        "research_count": case.research_count,
        "research_experience": case.research_experience,
        "publication_count": case.publication_count,
        "publications": case.publications,
        "work_years": case.work_years,
        "work_experience": case.work_experience,
        "extracurricular": case.extracurricular,
        "awards": case.awards,
        "recommendation_strength": case.recommendation_strength,
        "admitted_university_id": case.admitted_university_id,
        "admitted_major_id": case.admitted_major_id,
        "admission_year": case.admission_year,
        "admission_semester": case.admission_semester,
        "result": case.result,
        "scholarship": case.scholarship,
        "submitter_id": case.submitter_id,
        "is_verified": case.is_verified,
        "remarks": case.remarks,
        "created_at": case.created_at,
        "updated_at": case.updated_at,
        # 关联名称
        "undergraduate_university_display": (
            case.undergraduate_university.name if case.undergraduate_university 
            else case.undergraduate_university_name
        ),
        "admitted_university_name": case.admitted_university.name if case.admitted_university else None,
        "admitted_major_name": case.admitted_major.name if case.admitted_major else None,
        "admitted_country": case.admitted_university.country if case.admitted_university else None,
        "submitter_name": case.submitter.nickname if case.submitter else None,
    }


@router.get("", response_model=List[CaseResponse])
def get_cases(
    country: Optional[str] = Query(None, description="录取国家"),
    university_id: Optional[int] = Query(None, description="录取院校ID"),
    major_id: Optional[int] = Query(None, description="录取专业ID"),
    result: Optional[str] = Query(None, description="录取结果"),
    year: Optional[int] = Query(None, description="录取年份"),
    keyword: Optional[str] = Query(None, description="关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取录取案例列表"""
    query = db.query(Case).join(
        University, Case.admitted_university_id == University.id
    )
    
    if country:
        query = query.filter(University.country == country)
    if university_id:
        query = query.filter(Case.admitted_university_id == university_id)
    if major_id:
        query = query.filter(Case.admitted_major_id == major_id)
    if result:
        query = query.filter(Case.result == result)
    if year:
        query = query.filter(Case.admission_year == year)
    if keyword:
        query = query.filter(
            Case.applicant_name.contains(keyword) |
            Case.undergraduate_university_name.contains(keyword) |
            Case.undergraduate_major.contains(keyword)
        )
    
    cases = query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    return [_case_to_dict(c) for c in cases]


@router.get("/count")
def get_cases_count(
    country: Optional[str] = Query(None),
    university_id: Optional[int] = Query(None),
    major_id: Optional[int] = Query(None),
    result: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取案例总数（支持筛选）"""
    query = db.query(Case)
    if country:
        query = query.join(University, Case.admitted_university_id == University.id).filter(University.country == country)
    if university_id:
        query = query.filter(Case.admitted_university_id == university_id)
    if major_id:
        query = query.filter(Case.admitted_major_id == major_id)
    if result:
        query = query.filter(Case.result == result)
    if year:
        query = query.filter(Case.admission_year == year)
    if keyword:
        query = query.filter(
            Case.applicant_name.contains(keyword) |
            Case.undergraduate_university_name.contains(keyword) |
            Case.undergraduate_major.contains(keyword)
        )
    total = query.count()
    return {"total": total}


# ============================
# 模糊搜索 (自动完成) — 必须在 /{case_id} 之前声明
# ============================

@router.get("/search/universities")
def search_universities(
    q: str = Query("", min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """模糊搜索院校（用于自动完成下拉框）"""
    results = db.query(University).filter(
        University.name.contains(q) | University.name_en.contains(q)
    ).limit(limit).all()
    return [{"id": u.id, "name": u.name, "name_en": u.name_en, "country": u.country} for u in results]


@router.get("/search/majors")
def search_majors(
    q: str = Query("", min_length=1, description="搜索关键词"),
    university_id: Optional[int] = Query(None, description="院校ID筛选"),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """模糊搜索专业（用于自动完成下拉框）"""
    query = db.query(Major).filter(
        Major.name.contains(q) | Major.name_en.contains(q)
    )
    if university_id:
        query = query.filter(Major.university_id == university_id)
    results = query.limit(limit).all()
    return [{"id": m.id, "name": m.name, "name_en": m.name_en, "university_id": m.university_id} for m in results]


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    """获取案例详情"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    return _case_to_dict(case)


@router.post("", response_model=CaseResponse)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建录取案例"""
    # 验证录取院校和专业存在
    if not db.query(University).filter(University.id == case_data.admitted_university_id).first():
        raise HTTPException(status_code=400, detail="录取院校不存在")
    if not db.query(Major).filter(Major.id == case_data.admitted_major_id).first():
        raise HTTPException(status_code=400, detail="录取专业不存在")
    
    # 如果提供了本科院校ID，自动填充名称
    if case_data.undergraduate_university_id:
        uni = db.query(University).filter(University.id == case_data.undergraduate_university_id).first()
        if uni:
            case_data.undergraduate_university_name = uni.name
    
    new_case = Case(
        **case_data.model_dump(),
        submitter_id=current_user.id
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return _case_to_dict(new_case)


@router.put("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    update_data: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新录取案例（提交者或管理员）"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    
    if case.submitter_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="无权修改此案例")
    
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(case, field, value)
    
    db.commit()
    db.refresh(case)
    return _case_to_dict(case)


@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """删除录取案例（管理员）"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    
    db.delete(case)
    db.commit()
    return {"message": "案例已删除"}


# ============================
# AI 智能推荐
# ============================

@router.post("/recommend", response_model=List[RecommendationResult])
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    AI 智能推荐：根据用户背景条件，分析历史录取案例，推荐院校和专业
    返回按录取概率排序的推荐列表
    """
    results = generate_recommendations(request, db, top_k=15)
    return results
    return results
