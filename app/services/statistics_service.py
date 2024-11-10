from typing import Dict, List, Optional
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.match import Match
from app.models.player import Player
from app.models.tournament import Tournament

class StatisticsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_player_stats(self, player_id: int) -> Dict:
        """Get comprehensive statistics for a player."""
        # Get total matches
        total_wins = await self.db.query(Match).filter(
            Match.winner_id == player_id
        ).count()
        
        total_losses = await self.db.query(Match).filter(
            Match.loser_id == player_id
        ).count()
        
        total_matches = total_wins + total_losses
        
        # Calculate win rate
        win_rate = (total_wins / total