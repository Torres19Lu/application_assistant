from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import uuid
from app.config.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, UserUpdate, AdminUserCreate, AdminUserUpdate, AdminResetPassword
from app.utils.security import verify_password, get_password_hash, create_access_token, decode_token
from app.config.settings import get_settings

router = APIRouter(prefix="/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    return current_user

def get_optional_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)), db: Session = Depends(get_db)) -> Optional[User]:
    """可选的用户认证，未登录返回None"""
    if not token:
        return None
    payload = decode_token(token)
    if payload is None:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user if user and user.is_active else None

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        nickname=user_data.nickname or user_data.email.split('@')[0],
        phone=user_data.phone or None,
        target_country=user_data.target_country,
        target_major=user_data.target_major,
        role=UserRole.USER
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录（表单格式）"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户个人信息"""
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/password")
def change_password(
    password_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """修改密码"""
    old_password = password_data.get("old_password", "")
    new_password = password_data.get("new_password", "")
    
    if not old_password or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供旧密码和新密码"
        )
    
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码至少8位"
        )
    
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "密码修改成功"}

@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传用户头像"""
    settings = get_settings()
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG/PNG/GIF/WebP 格式的图片"
        )
    
    # 验证文件大小 (5MB)
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过5MB"
        )
    
    # 生成唯一文件名
    ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else 'jpg'
    filename = f"avatar_{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
    avatar_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    filepath = os.path.join(avatar_dir, filename)
    
    # 删除旧头像文件
    if current_user.avatar:
        old_path = current_user.avatar.lstrip('/')
        if os.path.exists(old_path):
            os.remove(old_path)
    
    # 保存文件
    with open(filepath, "wb") as f:
        f.write(content)
    
    # 更新数据库
    current_user.avatar = f"/uploads/avatars/{filename}"
    db.commit()
    db.refresh(current_user)
    return current_user

# ========== 管理员用户管理接口 ==========

@router.get("/users", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None),
    role: Optional[str] = Query(None, description="按角色筛选: user / admin"),
    status: Optional[str] = Query(None, description="按状态筛选: active / disabled"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """获取用户列表（管理员）"""
    query = db.query(User)
    if keyword:
        query = query.filter(
            User.email.contains(keyword) |
            User.nickname.contains(keyword) |
            User.phone.contains(keyword)
        )
    if role:
        query = query.filter(User.role == role)
    if status == "active":
        query = query.filter(User.is_active == 1)
    elif status == "disabled":
        query = query.filter(User.is_active == 0)
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users

@router.get("/users/count")
def get_users_count(
    keyword: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """获取用户总数（管理员）"""
    query = db.query(User)
    if keyword:
        query = query.filter(
            User.email.contains(keyword) |
            User.nickname.contains(keyword) |
            User.phone.contains(keyword)
        )
    if role:
        query = query.filter(User.role == role)
    if status == "active":
        query = query.filter(User.is_active == 1)
    elif status == "disabled":
        query = query.filter(User.is_active == 0)
    total = query.count()
    return {"total": total}

@router.post("/users", response_model=UserResponse)
def admin_create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """管理员创建用户（可创建管理员）"""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")

    role_enum = UserRole.ADMIN if user_data.role == "admin" else UserRole.USER
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        nickname=user_data.nickname or user_data.email.split('@')[0],
        phone=user_data.phone or None,
        role=role_enum,
        is_active=1,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=UserResponse)
def admin_update_user(
    user_id: int,
    update_data: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """管理员编辑用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    data = update_data.model_dump(exclude_unset=True)
    if "role" in data:
        if user.id == current_user.id:
            raise HTTPException(status_code=400, detail="不能修改自己的角色")
        data["role"] = UserRole.ADMIN if data["role"] == "admin" else UserRole.USER
    if "is_active" in data:
        if user.id == current_user.id:
            raise HTTPException(status_code=400, detail="不能禁用自己的账号")
    if "email" in data and data["email"] != user.email:
        existing = db.query(User).filter(User.email == data["email"], User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="该邮箱已被其他用户使用")

    # 空字符串 phone 转 None，避免唯一约束冲突
    if "phone" in data and not data["phone"]:
        data["phone"] = None
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

@router.put("/users/{user_id}/toggle")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """启用/禁用用户（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能操作自己的账号")
    
    user.is_active = 0 if user.is_active else 1
    db.commit()
    status_text = "启用" if user.is_active else "禁用"
    return {"message": f"用户已{status_text}"}

@router.put("/users/{user_id}/reset-password")
def admin_reset_password(
    user_id: int,
    password_data: AdminResetPassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """管理员重置用户密码"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "密码已重置"}

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """删除用户（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己的账号")
    
    db.delete(user)
    db.commit()
    return {"message": "用户已删除"}
