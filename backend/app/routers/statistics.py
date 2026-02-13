from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config.database import get_db
from app.models.university import University
from app.models.major import Major
from app.models.user import User
from app.models.guide import Guide
from app.models.collection import Collection

router = APIRouter(prefix="/statistics", tags=["统计"])

@router.get("")
def get_statistics(db: Session = Depends(get_db)):
    """获取平台统计数据"""
    university_count = db.query(University).count()
    major_count = db.query(Major).count()
    user_count = db.query(User).count()
    guide_count = db.query(Guide).count()
    collection_count = db.query(Collection).count()
    
    # 国家分布
    country_stats = db.query(
        University.country,
        func.count(University.id).label('count')
    ).group_by(University.country).all()
    
    # 专业分类统计
    category_stats = db.query(
        Major.category,
        func.count(Major.id).label('count')
    ).group_by(Major.category).all()
    
    return {
        "university_count": university_count,
        "major_count": major_count,
        "user_count": user_count,
        "guide_count": guide_count,
        "collection_count": collection_count,
        "country_distribution": [{"country": c[0], "count": c[1]} for c in country_stats],
        "category_distribution": [{"category": c[0], "count": c[1]} for c in category_stats]
    }
