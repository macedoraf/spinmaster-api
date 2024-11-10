from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MatchUpdate(BaseModel):
    player1_score: Optional[int] = Field(None, ge=0, description="Score of player 1")
    player2_score: Optional[int] = Field(None, ge=0, description="Score of player 2")
    tournament_id: Optional[int] = None

class SetCreate(BaseModel):
    set_number: int 
    score_p1: int 
    score_p2: int

class Set(SetCreate):
    id: int

class MatchBase(BaseModel):
    player1_id: int = Field(..., description="ID of the first player")
    player2_id: int = Field(..., description="ID of the second player")
    player1_score: int = Field(..., ge=0, description="Score of player 1")
    player2_score: int = Field(..., ge=0, description="Score of player 2")
    tournament_id: Optional[int] = Field(None, description="ID of the tournament if part of one")
    sets: List[Set]
    
class MatchCreate(MatchBase):
    player1_id: int
    player2_id: int
    tournament_id: Optional[int] = None
    sets: List[SetCreate]
 

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    winner_id: int 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True