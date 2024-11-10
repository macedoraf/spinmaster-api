from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.db.base import Base

class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    score_p1 = Column(Integer, nullable=False)
    score_p2 = Column(Integer, nullable=False)
    match = relationship("Match", back_populates="sets")

    __table_args__ = (
        UniqueConstraint('match_id', 'set_number', name='unique_set_number'),
    )