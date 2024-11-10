from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.player import Player
from app.models.ranking import RankingHistory
from app.utils.constants import K_FACTOR, RATING_SCALE

class RankingService:
    def __init__(self, db: Session):
        self.db = db

    async def calculate_elo_change(
        self, 
        winner_rating: float, 
        loser_rating: float
    ) -> float:
        """Calculate ELO rating change based on match result."""
        # Calculate expected scores
        expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / RATING_SCALE))
        expected_loser = 1 - expected_winner
        
        # Calculate rating changes
        winner_change = K_FACTOR * (1 - expected_winner)
        loser_change = K_FACTOR * (0 - expected_loser)
        
        return winner_change, loser_change

    async def update_ratings_after_match(
        self, 
        winner: Player, 
        loser: Player
    ) -> None:
        """Update players' ratings after a match."""
        winner_change, loser_change = await self.calculate_elo_change(
            winner.rating,
            loser.rating
        )
        
        # Create rating history records
        winner_history = RankingHistory(
            player_id=winner.id,
            old_rating=winner.rating,
            new_rating=winner.rating + winner_change,
            change=winner_change,
            timestamp=datetime.now()
        )
        
        loser_history = RankingHistory(
            player_id=loser.id,
            old_rating=loser.rating,
            new_rating=loser.rating + loser_change,
            change=loser_change,
            timestamp=datetime.now()
        )
        
        # Update current ratings
        winner.rating += winner_change
        loser.rating += loser_change
        
        # Save changes
        self.db.add(winner_history)
        self.db.add(loser_history)
        
        try:
            await self.db.flush()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_rankings(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Player]:
        """Get current rankings ordered by rating."""
        return await self.db.query(Player).filter(
            Player.active == True
        ).order_by(Player.rating.desc()).offset(skip).limit(limit).all()

    async def get_player_history(
        self, 
        player_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[RankingHistory]:
        """Get rating history for a specific player."""
        return await self.db.query(RankingHistory).filter(
            RankingHistory.player_id == player_id
        ).order_by(RankingHistory.timestamp.desc()).offset(skip).limit(limit).all()

    async def get_rating_timeline(
        self, 
        player_id: int,
        days: int = 30
    ) -> List[RankingHistory]:
        """Get player's rating timeline for the specified number of days."""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return await self.db.query(RankingHistory).filter(
            RankingHistory.player_id == player_id,
            RankingHistory.timestamp >= cutoff_date
        ).order_by(RankingHistory.timestamp.asc()).all()
