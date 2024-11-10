from sqlalchemy import Column, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class MatchType(enum.Enum):
    FRIENDLY = "friendly"
    TOURNAMENT = "tournament"
    CHALLENGE = "challenge"

class Match(Base, TimestampMixin):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player1_score = Column(Integer, nullable=False)
    player2_score = Column(Integer, nullable=False)
    match_type = Column(Enum(MatchType), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=True)
    notes = Column(String(500))
    
    # Relationships
    player1 = relationship("Player", back_populates="matches_as_player1", foreign_keys=[player1_id])
    player2 = relationship("Player", back_populates="matches_as_player2", foreign_keys=[player2_id])
    tournament = relationship("Tournament", back_populates="matches")
