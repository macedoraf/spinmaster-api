from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class TournamentType(str, Enum):
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    ROUND_ROBIN = "round_robin"
    GROUP_STAGE = "group_stage"

class TournamentStatus(str, Enum):
    DRAFT = "draft"
    REGISTRATION = "registration"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TournamentBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    tournament_type: TournamentType
    start_date: datetime
    end_date: datetime
    max_players: int = Field(..., ge=4, le=128)
    min_player_rating: Optional[float] = None
    max_player_rating: Optional[float] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class TournamentCreate(TournamentBase):
    pass

class TournamentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    tournament_type: Optional[TournamentType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[TournamentStatus] = None

class Tournament(TournamentBase):
    id: int
    status: TournamentStatus = TournamentStatus.DRAFT
    created_at: datetime
    updated_at: datetime
    registered_players: int = 0
    current_round: int = 0
    winner_id: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TournamentList(BaseModel):
    id: int
    name: str
    tournament_type: TournamentType
    start_date: datetime
    status: TournamentStatus
    registered_players: int
    max_players: int

    class Config:
        from_attributes = True

class TournamentRegistration(BaseModel):
    player_id: int
    tournament_id: int
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    seed: Optional[int] = None
