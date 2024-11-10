from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

class PlayerCategory(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

class PlayerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, pattern=r"^\+?1?\d{9,15}$")
    category: PlayerCategory = Field(default=PlayerCategory.F)
    is_active: bool = Field(default=True)

class PlayerCreate(PlayerBase):
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "nickname": "Johnny",
                "phone": "+5511999999999",
                "category": "F",
                "password": "strongpassword123"
            }
        }

class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, pattern=r"^\+?1?\d{9,15}$")
    category: Optional[PlayerCategory] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe Updated",
                "nickname": "John",
                "phone": "+5511999999999",
                "category": "E",
                "is_active": True
            }
        }

class PlayerResponse(PlayerBase):
    id: int
    elo_rating: int = Field(default=1000)
    matches_played: int = Field(default=0)
    matches_won: int = Field(default=0)
    matches_lost: int = Field(default=0)
    win_rate: float = Field(default=0.0)
    current_streak: int = Field(default=0)
    best_streak: int = Field(default=0)
    created_at: datetime
    updated_at: datetime

    @validator('win_rate')
    def calculate_win_rate(cls, v, values):
        matches_played = values.get('matches_played', 0)
        matches_won = values.get('matches_won', 0)
        if matches_played > 0:
            return round((matches_won / matches_played) * 100, 2)
        return 0.0

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "nickname": "Johnny",
                "phone": "+5511999999999",
                "category": "F",
                "is_active": True,
                "elo_rating": 1000,
                "matches_played": 10,
                "matches_won": 6,
                "matches_lost": 4,
                "win_rate": 60.0,
                "current_streak": 2,
                "best_streak": 3,
                "created_at": "2024-02-10T10:00:00",
                "updated_at": "2024-02-10T10:00:00"
            }
        }

class PlayerInRanking(BaseModel):
    id: int
    name: str
    nickname: Optional[str]
    category: PlayerCategory
    elo_rating: int
    position: int
    previous_position: Optional[int]
    matches_played: int
    win_rate: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "nickname": "Johnny",
                "category": "F",
                "elo_rating": 1000,
                "position": 1,
                "previous_position": 2,
                "matches_played": 10,
                "win_rate": 60.0
            }
        }