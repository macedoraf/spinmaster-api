from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.utils.constants import INITIAL_RATING

class PlayerService:
    def __init__(self, db: Session):
        self.db = db

    async def create_player(self, player: PlayerCreate) -> Player:
        """Create a new player with initial rating."""
        db_player = Player(
            name=player.name,
            email=player.email,
            rating=INITIAL_RATING,
            active=True
        )
        self.db.add(db_player)
        try:
            await self.db.flush()
            await self.db.refresh(db_player)
            return db_player
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_player(self, player_id: int) -> Optional[Player]:
        """Get player by ID."""
        return await self.db.query(Player).filter(Player.id == player_id).first()

    async def get_players(self, skip: int = 0, limit: int = 100) -> List[Player]:
        """Get list of players with pagination."""
        return await self.db.query(Player).offset(skip).limit(limit).all()

    async def update_player(self, player_id: int, player_update: PlayerUpdate) -> Optional[Player]:
        """Update player information."""
        db_player = await self.get_player(player_id)
        if not db_player:
            raise HTTPException(status_code=404, detail="Player not found")
        
        update_data = player_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_player, field, value)
        
        try:
            await self.db.flush()
            await self.db.refresh(db_player)
            return db_player
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def deactivate_player(self, player_id: int) -> bool:
        """Deactivate a player (soft delete)."""
        db_player = await self.get_player(player_id)
        if not db_player:
            raise HTTPException(status_code=404, detail="Player not found")
        
        db_player.active = False
        try:
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_player_by_email(self, email: str) -> Optional[Player]:
        """Get player by email."""
        return await self.db.query(Player).filter(Player.email == email).first()