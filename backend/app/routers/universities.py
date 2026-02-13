from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.models.university import University
from app.models.major import Major
from app.schemas.university import UniversityCreate, UniversityResponse, UniversityUpdate
from app.routers.auth import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/universities", tags=["院校"])

@router.get("", response_model=List[UniversityResponse])
def get_universities(
    country: Optional[str] = Query(None, description="国家/地区"),
    difficulty: Optional[str] = Query(None, description="申请难度"),
    min_ranking: Optional[int] = Query(None, description="最低排名"),
    max_ranking: Optional[int] = Query(None, description="最高排名"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    sort_by: Optional[str] = Query(None, description="排序方式: ranking / name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取院校列表"""
    query = db.query(University)
    
    if country:
        query = query.filter(University.country == country)
    if difficulty:
        query = query.filter(University.difficulty == difficulty)
    if min_ranking:
        query = query.filter(University.qs_ranking >= min_ranking)
    if max_ranking:
        query = query.filter(University.qs_ranking <= max_ranking)
    if keyword:
        query = query.filter(
            University.name.contains(keyword) | 
            University.name_en.contains(keyword)
        )
    
    if sort_by == "name":
        query = query.order_by(University.name)
    else:
        query = query.order_by(University.qs_ranking)
    
    universities = query.offset(skip).limit(limit).all()
    return universities

@router.get("/count")
def get_universities_count(
    country: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    min_ranking: Optional[int] = Query(None),
    max_ranking: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取院校总数（支持筛选）"""
    query = db.query(University)
    if country:
        query = query.filter(University.country == country)
    if difficulty:
        query = query.filter(University.difficulty == difficulty)
    if min_ranking:
        query = query.filter(University.qs_ranking >= min_ranking)
    if max_ranking:
        query = query.filter(University.qs_ranking <= max_ranking)
    if keyword:
        query = query.filter(
            University.name.contains(keyword) |
            University.name_en.contains(keyword)
        )
    total = query.count()
    return {"total": total}

@router.get("/{university_id}", response_model=UniversityResponse)
def get_university(university_id: int, db: Session = Depends(get_db)):
    """获取院校详情"""
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院校不存在"
        )
    return university

@router.post("", response_model=UniversityResponse)
def create_university(
    university_data: UniversityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """创建院校（管理员）"""
    university = University(**university_data.dict())
    db.add(university)
    db.commit()
    db.refresh(university)
    return university

@router.put("/{university_id}", response_model=UniversityResponse)
def update_university(
    university_id: int,
    university_data: UniversityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """更新院校（管理员）"""
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院校不存在"
        )
    
    for field, value in university_data.dict(exclude_unset=True).items():
        setattr(university, field, value)
    
    db.commit()
    db.refresh(university)
    return university

@router.delete("/{university_id}")
def delete_university(
    university_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """删除院校（管理员）"""
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院校不存在"
        )
    
    db.delete(university)
    db.commit()
    return {"message": "院校已删除"}

@router.get("/{university_id}/majors")
def get_university_majors(
    university_id: int,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取院校的专业列表"""
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="院校不存在"
        )
    
    query = db.query(Major).filter(Major.university_id == university_id)
    if category:
        query = query.filter(Major.category == category)
    
    majors = query.all()
    return majors
