from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas import PlayerCreate, PlayerUpdate, PlayerResponse
from app.services import player_service

router = APIRouter()

@router.post("/", response_model=PlayerResponse)
def create_player(
    player: PlayerCreate,
    db: Session = Depends(deps.get_db)
):
    """Create a new player"""
    return player_service.create_player(db=db, player=player)

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int = Path(..., title="The ID of the player to get"),
    db: Session = Depends(deps.get_db)
):
    """Get player by ID"""
    player = player_service.get_player(db=db, player_id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/", response_model=List[PlayerResponse])
def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(deps.get_db)
):
    """List all players with pagination"""
    return player_service.get_players(db=db, skip=skip, limit=limit)

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int,
    player: PlayerUpdate,
    db: Session = Depends(deps.get_db)
):
    """Update player information"""
    updated_player = player_service.update_player(db=db, player_id=player_id, player=player)
    if not updated_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

@router.delete("/{player_id}")
def delete_player(
    player_id: int = Path(..., title="The ID of the player to delete"),
    db: Session = Depends(deps.get_db)
):
    """Delete a player"""
    success = player_service.delete_player(db=db, player_id=player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player successfully deleted"}