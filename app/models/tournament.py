from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class TournamentStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Tournament(Base, TimestampMixin):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(TournamentStatus), default=TournamentStatus.PENDING)
    max_players = Column(Integer)
    is_ranked = Column(Boolean, default=True)
    
    # Relationships
    matches = relationship("Match", back_populates="tournament")
    tournament_players = relationship("TournamentPlayer", back_populates="tournament")
