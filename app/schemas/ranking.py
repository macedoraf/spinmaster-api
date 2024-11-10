from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class RankingPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    ALL_TIME = "all_time"

class RankingType(str, Enum):
    GENERAL = "general"
    TOURNAMENT = "tournament"
    LEVEL_BASED = "level_based"

class RankingEntry(BaseModel):
    player_id: int
    rating: float
    rank: int
    previous_rank: Optional[int] = None
    matches_played: int
    win_rate: float
    rating_change: float
    ranking_period: RankingPeriod
    ranking_type: RankingType
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class RankingList(BaseModel):
    entries: List[RankingEntry]
    total_players: int
    ranking_period: RankingPeriod
    ranking_type: RankingType
    generated_at: datetime

class RankingHistory(BaseModel):
    player_id: int
    rating_history: List[float]
    rank_history: List[int]
    timestamps: List[datetime]

class RankingStats(BaseModel):
    highest_rating: float
    highest_rating_date: datetime
    lowest_rating: float
    lowest_rating_date: datetime
    best_rank: int
    best_rank_date: datetime
    rating_change_30d: float
    rank_change_30d: int

class RankingFilter(BaseModel):
    ranking_period: Optional[RankingPeriod] = None
    ranking_type: Optional[RankingType] = None
    min_matches: Optional[int] = None
    player_level: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
