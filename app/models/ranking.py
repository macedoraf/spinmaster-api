from sqlalchemy import Column, Integer, ForeignKey, Float, Date, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Ranking(Base, TimestampMixin):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    points = Column(Float, nullable=False)
    rank_date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False)
    
    # Relationship
    player = relationship("Player")
