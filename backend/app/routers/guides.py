from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.models.guide import Guide
from app.schemas.guide import GuideCreate, GuideResponse, GuideUpdate
from app.routers.auth import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/guides", tags=["申请攻略"])

@router.get("", response_model=List[GuideResponse])
def get_guides(
    category: Optional[str] = Query(None, description="分类"),
    subcategory: Optional[str] = Query(None, description="子分类"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    is_pinned: Optional[bool] = Query(None, description="是否置顶"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取攻略列表"""
    query = db.query(Guide)
    
    if category:
        query = query.filter(Guide.category == category)
    if subcategory:
        query = query.filter(Guide.subcategory == subcategory)
    if is_pinned is not None:
        query = query.filter(Guide.is_pinned == (1 if is_pinned else 0))
    if keyword:
        query = query.filter(
            Guide.title.contains(keyword) | 
            Guide.content.contains(keyword)
        )
    
    guides = query.order_by(Guide.is_pinned.desc(), Guide.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for guide in guides:
        result.append({
            "id": guide.id,
            "title": guide.title,
            "category": guide.category,
            "subcategory": guide.subcategory,
            "content": guide.content,
            "summary": guide.summary,
            "cover_image": guide.cover_image,
            "views": guide.views,
            "likes": guide.likes,
            "is_pinned": guide.is_pinned,
            "author_id": guide.author_id,
            "author_name": guide.author.nickname if guide.author else None,
            "created_at": guide.created_at,
            "updated_at": guide.updated_at
        })
    
    return result

@router.get("/count")
def get_guides_count(
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取攻略总数（支持筛选）"""
    query = db.query(Guide)
    if category:
        query = query.filter(Guide.category == category)
    if subcategory:
        query = query.filter(Guide.subcategory == subcategory)
    if keyword:
        query = query.filter(
            Guide.title.contains(keyword) |
            Guide.content.contains(keyword)
        )
    total = query.count()
    return {"total": total}

@router.get("/{guide_id}", response_model=GuideResponse)
def get_guide(guide_id: int, db: Session = Depends(get_db)):
    """获取攻略详情"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="攻略不存在"
        )
    
    guide.views += 1
    db.commit()
    
    return {
        "id": guide.id,
        "title": guide.title,
        "category": guide.category,
        "subcategory": guide.subcategory,
        "content": guide.content,
        "summary": guide.summary,
        "cover_image": guide.cover_image,
        "views": guide.views,
        "likes": guide.likes,
        "is_pinned": guide.is_pinned,
        "author_id": guide.author_id,
        "author_name": guide.author.nickname if guide.author else None,
        "created_at": guide.created_at,
        "updated_at": guide.updated_at
    }

@router.post("", response_model=GuideResponse)
def create_guide(
    guide_data: GuideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """创建攻略（管理员）"""
    guide = Guide(
        **guide_data.dict(),
        author_id=current_user.id
    )
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return guide

@router.put("/{guide_id}", response_model=GuideResponse)
def update_guide(
    guide_id: int,
    guide_data: GuideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """更新攻略（管理员）"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="攻略不存在"
        )
    
    for field, value in guide_data.dict(exclude_unset=True).items():
        setattr(guide, field, value)
    
    db.commit()
    db.refresh(guide)
    return guide

@router.delete("/{guide_id}")
def delete_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """删除攻略（管理员）"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="攻略不存在"
        )
    
    db.delete(guide)
    db.commit()
    return {"message": "攻略已删除"}

@router.post("/{guide_id}/like")
def like_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """点赞攻略"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="攻略不存在"
        )
    
    guide.likes += 1
    db.commit()
    return {"message": "点赞成功", "likes": guide.likes}
