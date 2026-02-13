from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nickname: Optional[str] = ""
    phone: Optional[str] = None
    target_country: Optional[str] = ""
    target_major: Optional[str] = ""
    avatar: Optional[str] = ""

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    phone: Optional[str] = None
    target_country: Optional[str] = None
    target_major: Optional[str] = None
    avatar: Optional[str] = None

class AdminUserCreate(BaseModel):
    """管理员创建用户"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    nickname: Optional[str] = ""
    phone: Optional[str] = None
    role: Optional[str] = "user"  # user / admin

class AdminUserUpdate(BaseModel):
    """管理员编辑用户"""
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    target_country: Optional[str] = None
    target_major: Optional[str] = None
    is_active: Optional[int] = None

class AdminResetPassword(BaseModel):
    """管理员重置密码"""
    new_password: str = Field(..., min_length=6)
