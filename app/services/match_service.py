from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.match import Match
from app.models.player import Player
from app.schemas.match import MatchCreate
from app.services.ranking_service import RankingService
from app.db.session import get_db

class MatchService:
    def __init__(self):
        self.db = get_db()
        self.ranking_service = RankingService()

    async def create_match(self, match: MatchCreate) -> Match:
        """Create a new match and update players' ratings."""
        # Verify both players exist and are active
        winner = await self.db.query(Player).filter(
            Player.id == match.winner_id, 
            Player.active == True
        ).first()
        loser = await self.db.query(Player).filter(
            Player.id == match.loser_id, 
            Player.active == True
        ).first()

        if not winner or not loser:
            raise HTTPException(status_code=404, detail="One or both players not found or inactive")

        # Create match record
        db_match = Match(
            winner_id=match.winner_id,
            loser_id=match.loser_id,
            score=match.score,
            tournament_id=match.tournament_id,
            match_date=datetime.now()
        )
        self.db.add(db_match)

        try:
            # Update rankings
            await self.ranking_service.update_ratings_after_match(winner, loser)
            await self.db.flush()
            await self.db.refresh(db_match)
            return db_match
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_match(self, match_id: int) -> Optional[Match]:
        """Get match by ID."""
        return await self.db.query(Match).filter(Match.id == match_id).first()

    async def get_player_matches(
        self, 
        player_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Match]:
        """Get all matches for a specific player."""
        return await self.db.query(Match).filter(
            (Match.winner_id == player_id) | (Match.loser_id == player_id)
        ).order_by(Match.match_date.desc()).offset(skip).limit(limit).all()

    async def get_head_to_head(
        self, 
        player1_id: int, 
        player2_id: int
    ) -> Tuple[int, int]:
        """Get head-to-head record between two players."""
        player1_wins = await self.db.query(Match).filter(
            Match.winner_id == player1_id,
            Match.loser_id == player2_id
        ).count()
        
        player2_wins = await self.db.query(Match).filter(
            Match.winner_id == player2_id,
            Match.loser_id == player1_id
        ).count()
        
        return (player1_wins, player2_wins)
