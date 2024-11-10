from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tournament import Tournament, TournamentPlayer
from app.models.match import Match
from app.schemas.tournament import TournamentCreate, TournamentUpdate
from app.utils.constants import TOURNAMENT_STATUSES

class TournamentService:
    def __init__(self, db: Session):
        self.db = db

    async def create_tournament(self, tournament: TournamentCreate) -> Tournament:
        """Create a new tournament."""
        db_tournament = Tournament(
            name=tournament.name,
            start_date=tournament.start_date,
            end_date=tournament.end_date,
            max_players=tournament.max_players,
            status=TOURNAMENT_STATUSES['PENDING']
        )
        self.db.add(db_tournament)
        
        try:
            await self.db.flush()
            await self.db.refresh(db_tournament)
            return db_tournament
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        """Get tournament by ID."""
        return await self.db.query(Tournament).filter(Tournament.id == tournament_id).first()

    async def update_tournament(
        self, 
        tournament_id: int, 
        tournament_update: TournamentUpdate
    ) -> Tournament:
        """Update tournament details."""
        db_tournament = await self.get_tournament(tournament_id)
        if not db_tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")
        
        update_data = tournament_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tournament, field, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(db_tournament)
            return db_tournament
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def register_player(self, tournament_id: int, player_id: int) -> bool:
        """Register a player for a tournament."""
        tournament = await self.get_tournament(tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")
            
        if tournament.status != TOURNAMENT_STATUSES['PENDING']:
            raise HTTPException(status_code=400, detail="Tournament registration is closed")
            
        current_players = await self.db.query(TournamentPlayer).filter(
            TournamentPlayer.tournament_id == tournament_id
        ).count()
        
        if current_players >= tournament.max_players:
            raise HTTPException(status_code=400, detail="Tournament is full")
            
        tournament_player = TournamentPlayer(
            tournament_id=tournament_id,
            player_id=player_id
        )
        self.db.add(tournament_player)
        
        try:
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_tournament_standings(self, tournament_id: int) -> List[Dict]:
        """Get tournament standings based on matches played."""
        matches = await self.db.query(Match).filter(
            Match.tournament_id == tournament_id
        ).all()
        
        standings = {}
        for match in matches:
            # Initialize players if not in standings
            if match.winner_id not in standings:
                standings[match.winner_id] = {'wins': 0, 'losses': 0}
            if match.loser_id not in standings:
                standings[match.loser_id] = {'wins': 0, 'losses': 0}
                
            # Update standings
            standings[match.winner_id]['wins'] += 1
            standings[match.loser_id]['losses'] += 1
        
        # Convert to list and sort by wins
        return sorted(
            [{'player_id': k, **v} for k, v in standings.items()],
            key=lambda x: x['wins'],
            reverse=True
        )
