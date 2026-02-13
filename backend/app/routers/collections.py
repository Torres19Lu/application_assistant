from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.models.collection import Collection
from app.models.university import University
from app.models.major import Major
from app.schemas.collection import CollectionCreate, CollectionResponse
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/collections", tags=["收藏"])

@router.get("", response_model=List[CollectionResponse])
def get_collections(
    collection_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的收藏列表"""
    query = db.query(Collection).filter(Collection.user_id == current_user.id)
    
    if collection_type:
        query = query.filter(Collection.collection_type == collection_type)
    
    collections = query.order_by(Collection.created_at.desc()).all()
    
    result = []
    for collection in collections:
        target = None
        if collection.collection_type == "university":
            uni = db.query(University).filter(University.id == collection.target_id).first()
            if uni:
                target = {
                    "id": uni.id,
                    "name": uni.name,
                    "name_en": uni.name_en,
                    "country": uni.country,
                    "logo_url": uni.logo_url,
                }
        elif collection.collection_type == "major":
            major = db.query(Major).filter(Major.id == collection.target_id).first()
            if major:
                target = {
                    "id": major.id,
                    "name": major.name,
                    "university_name": major.university.name if major.university else None
                }
        
        result.append({
            "id": collection.id,
            "user_id": collection.user_id,
            "collection_type": collection.collection_type,
            "target_id": collection.target_id,
            "created_at": collection.created_at,
            "target": target
        })
    
    return result

@router.post("", response_model=CollectionResponse)
def add_collection(
    collection_data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加收藏"""
    existing = db.query(Collection).filter(
        Collection.user_id == current_user.id,
        Collection.collection_type == collection_data.collection_type,
        Collection.target_id == collection_data.target_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过了"
        )
    
    if collection_data.collection_type == "university":
        target = db.query(University).filter(University.id == collection_data.target_id).first()
    elif collection_data.collection_type == "major":
        target = db.query(Major).filter(Major.id == collection_data.target_id).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的收藏类型"
        )
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏目标不存在"
        )
    
    collection = Collection(
        user_id=current_user.id,
        collection_type=collection_data.collection_type,
        target_id=collection_data.target_id
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    
    # 将 target 转为可序列化的字典
    target_data = None
    if collection_data.collection_type == "university" and target:
        target_data = {
            "id": target.id,
            "name": target.name,
            "name_en": target.name_en,
            "country": target.country,
            "logo_url": target.logo_url,
        }
    elif collection_data.collection_type == "major" and target:
        target_data = {
            "id": target.id,
            "name": target.name,
            "university_name": target.university.name if target.university else None,
        }

    return {
        "id": collection.id,
        "user_id": collection.user_id,
        "collection_type": collection.collection_type,
        "target_id": collection.target_id,
        "created_at": collection.created_at,
        "target": target_data
    }

@router.delete("/{collection_id}")
def remove_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """取消收藏"""
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏记录不存在"
        )
    
    db.delete(collection)
    db.commit()
    return {"message": "已取消收藏"}

@router.get("/check")
def check_collection(
    type: str,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """检查是否已收藏"""
    collection = db.query(Collection).filter(
        Collection.user_id == current_user.id,
        Collection.collection_type == type,
        Collection.target_id == id
    ).first()
    
    return {"is_collected": collection is not None, "collection_id": collection.id if collection else None}
