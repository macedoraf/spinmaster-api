from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class TournamentPlayer(Base, TimestampMixin):
    __tablename__ = "tournament_players"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    final_position = Column(Integer)
    
    # Relationships
    tournament = relationship("Tournament", back_populates="tournament_players")
    player = relationship("Player", back_populates="tournament_players")
