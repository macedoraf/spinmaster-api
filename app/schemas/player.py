from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator

class PlayerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = None
    is_active: bool = True

class PlayerCreate(PlayerBase):
    password: str = Field(..., min_length=8)

class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)

class Player(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    current_rating: float = 1000.0
    highest_rating: float = 1000.0
    matches_played: int = 0
    wins: int = 0
    losses: int = 0

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PlayerInDB(Player):
    hashed_password: str

class PlayerList(BaseModel):
    id: int
    name: str
    nickname: Optional[str]
    current_rating: float
    matches_played: int

    class Config:
        from_attributes = True

class PlayerStats(BaseModel):
    matches_played: int
    wins: int
    losses: int
    win_rate: float
    current_rating: float
    highest_rating: float
    rating_change_30d: float
    best_victory_rating: Optional[float]
    longest_streak: int
    current_streak: int
