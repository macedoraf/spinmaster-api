from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
import re

class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=100)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match("^[a-zA-Z0-9_-]+$", v):
            raise ValueError('username must be alphanumeric')
        return v

class PlayerCreate(PlayerBase):
    password: str = Field(..., min_length=8)

class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('avatar_url')
    def validate_avatar_url(cls, v):
        if v is not None:
            # Validação básica de URL
            if not v.startswith(('http://', 'https://')):
                raise ValueError('avatar_url must be a valid URL')
        return v

class Player(PlayerBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    avatar_url: Optional[HttpUrl] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class PlayerInDB(Player):
    hashed_password: str