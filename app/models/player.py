from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class PlayerCategory(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"

class Player(Base, TimestampMixin):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    points = Column(Float, default=1000)
    category = Column(Enum(PlayerCategory), default=PlayerCategory.BEGINNER)
    is_active = Column(Boolean, default=True)
    total_matches = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # Relationships
    matches_as_player1 = relationship("Match", back_populates="player1", foreign_keys="Match.player1_id")
    matches_as_player2 = relationship("Match", back_populates="player2", foreign_keys="Match.player2_id")
    tournament_players = relationship("TournamentPlayer", back_populates="player")
