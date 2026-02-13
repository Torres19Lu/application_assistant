from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.models.major import Major
from app.models.university import University
from app.schemas.major import MajorCreate, MajorResponse, MajorUpdate
from app.routers.auth import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/majors", tags=["专业"])

@router.get("", response_model=List[MajorResponse])
def get_majors(
    category: Optional[str] = Query(None, description="学科大类"),
    subcategory: Optional[str] = Query(None, description="细分专业"),
    country: Optional[str] = Query(None, description="国家"),
    university_id: Optional[int] = Query(None, description="院校ID"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    sort_by: Optional[str] = Query(None, description="排序方式: default / ranking / admission"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取专业列表"""
    query = db.query(Major).join(University)
    
    if category:
        query = query.filter(Major.category == category)
    if subcategory:
        query = query.filter(Major.subcategory == subcategory)
    if country:
        query = query.filter(University.country == country)
    if university_id:
        query = query.filter(Major.university_id == university_id)
    if keyword:
        query = query.filter(
            Major.name.contains(keyword) | 
            Major.name_en.contains(keyword)
        )
    
    if sort_by == "ranking":
        query = query.order_by(University.qs_ranking)
    elif sort_by == "admission":
        query = query.order_by(Major.admission_rate.desc().nullslast())
    else:
        query = query.order_by(Major.id)
    
    majors = query.offset(skip).limit(limit).all()
    
    result = []
    for major in majors:
        major_dict = {
            "id": major.id,
            "name": major.name,
            "name_en": major.name_en,
            "category": major.category,
            "subcategory": major.subcategory,
            "university_id": major.university_id,
            "duration": major.duration,
            "tuition": major.tuition,
            "ielts_requirement": major.ielts_requirement,
            "toefl_requirement": major.toefl_requirement,
            "gpa_requirement": major.gpa_requirement,
            "gre_requirement": major.gre_requirement,
            "gmat_requirement": major.gmat_requirement,
            "description": major.description,
            "curriculum": major.curriculum,
            "career_prospects": major.career_prospects,
            "admission_rate": major.admission_rate,
            "avg_gpa": major.avg_gpa,
            "avg_ielts": major.avg_ielts,
            "total_admitted": major.total_admitted,
            "created_at": major.created_at,
            "updated_at": major.updated_at,
            "university_name": major.university.name if major.university else None,
            "university_logo": major.university.logo_url if major.university else None,
            "country": major.university.country if major.university else None
        }
        result.append(major_dict)
    
    return result

@router.get("/count")
def get_majors_count(
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    university_id: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取专业总数（支持筛选）"""
    query = db.query(Major).join(University)
    if category:
        query = query.filter(Major.category == category)
    if subcategory:
        query = query.filter(Major.subcategory == subcategory)
    if country:
        query = query.filter(University.country == country)
    if university_id:
        query = query.filter(Major.university_id == university_id)
    if keyword:
        query = query.filter(
            Major.name.contains(keyword) |
            Major.name_en.contains(keyword)
        )
    total = query.count()
    return {"total": total}

@router.get("/{major_id}", response_model=MajorResponse)
def get_major(major_id: int, db: Session = Depends(get_db)):
    """获取专业详情"""
    major = db.query(Major).filter(Major.id == major_id).first()
    if not major:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="专业不存在"
        )
    
    major_dict = {
        "id": major.id,
        "name": major.name,
        "name_en": major.name_en,
        "category": major.category,
        "subcategory": major.subcategory,
        "university_id": major.university_id,
        "duration": major.duration,
        "tuition": major.tuition,
        "ielts_requirement": major.ielts_requirement,
        "toefl_requirement": major.toefl_requirement,
        "gpa_requirement": major.gpa_requirement,
        "gre_requirement": major.gre_requirement,
        "gmat_requirement": major.gmat_requirement,
        "description": major.description,
        "curriculum": major.curriculum,
        "career_prospects": major.career_prospects,
        "admission_rate": major.admission_rate,
        "avg_gpa": major.avg_gpa,
        "avg_ielts": major.avg_ielts,
        "total_admitted": major.total_admitted,
        "created_at": major.created_at,
        "updated_at": major.updated_at,
        "university_name": major.university.name if major.university else None,
        "university_logo": major.university.logo_url if major.university else None,
        "country": major.university.country if major.university else None
    }
    
    return major_dict

@router.post("", response_model=MajorResponse)
def create_major(
    major_data: MajorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """创建专业（管理员）"""
    university = db.query(University).filter(University.id == major_data.university_id).first()
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院校不存在"
        )
    
    major = Major(**major_data.dict())
    db.add(major)
    db.commit()
    db.refresh(major)
    return major

@router.put("/{major_id}", response_model=MajorResponse)
def update_major(
    major_id: int,
    major_data: MajorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """更新专业（管理员）"""
    major = db.query(Major).filter(Major.id == major_id).first()
    if not major:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="专业不存在"
        )
    
    for field, value in major_data.dict(exclude_unset=True).items():
        setattr(major, field, value)
    
    db.commit()
    db.refresh(major)
    return major

@router.delete("/{major_id}")
def delete_major(
    major_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """删除专业（管理员）"""
    major = db.query(Major).filter(Major.id == major_id).first()
    if not major:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="专业不存在"
        )
    
    db.delete(major)
    db.commit()
    return {"message": "专业已删除"}
