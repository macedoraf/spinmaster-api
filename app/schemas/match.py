from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class MatchType(str, Enum):
    FRIENDLY = "friendly"
    TOURNAMENT = "tournament"
    CHALLENGE = "challenge"

class MatchResult(str, Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    WALKOVER = "walkover"

class GameScore(BaseModel):
    player_score: int = Field(..., ge=0, le=11)
    opponent_score: int = Field(..., ge=0, le=11)

    @validator('player_score', 'opponent_score')
    def validate_score(cls, v):
        if not (0 <= v <= 11):
            raise ValueError('Score must be between 0 and 11')
        return v

class MatchBase(BaseModel):
    match_type: MatchType
    player_id: int
    opponent_id: int
    tournament_id: Optional[int] = None
    notes: Optional[str] = None

class MatchCreate(MatchBase):
    games: List[GameScore]
    
    @validator('games')
    def validate_games(cls, v):
        if not (3 <= len(v) <= 5):  # Best of 5 format
            raise ValueError('Match must have between 3 and 5 games')
        return v

class MatchUpdate(BaseModel):
    notes: Optional[str] = None
    is_validated: Optional[bool] = None

class Match(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime
    games: List[GameScore]
    winner_id: int
    loser_id: int
    points_gained: float
    points_lost: float
    is_validated: bool = False

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MatchList(BaseModel):
    id: int
    match_type: MatchType
    player_id: int
    opponent_id: int
    winner_id: int
    created_at: datetime
    points_gained: float

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MatchFilter(BaseModel):
    player_id: Optional[int] = None
    opponent_id: Optional[int] = None
    match_type: Optional[MatchType] = None
    tournament_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_validated: Optional[bool] = None

class MatchStats(BaseModel):
    total_matches: int
    wins: int
    losses: int
    win_rate: float
    average_points_gained: float
    best_win_points: float
    longest_win_streak: int
    current_streak: int
