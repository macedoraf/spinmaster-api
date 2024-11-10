from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class SetCreate(BaseModel):
    set_number: int 
    score_p1: int 
    score_p2: int

class Set(SetCreate):
    id: int

class MatchBase(BaseModel):
    player1_id: int = Field(..., description="ID of the first player")
    player2_id: int = Field(..., description="ID of the second player")
    sets: List[SetCreate]
    tournament_id: Optional[int] = Field(None, description="ID of the tournament if part of one")

class MatchUpdate(MatchBase):
    pass
    
class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id : int
    
    class Config:
        from_attributes = True