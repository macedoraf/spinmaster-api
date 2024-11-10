from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.services.player_service import PlayerService
from app.schemas.player import Player, PlayerCreate, PlayerUpdate

router = APIRouter()

@router.post("/", response_model=Player, status_code=status.HTTP_201_CREATED)
def create_player(
    player_in: PlayerCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Criar novo jogador
    """
    player_service = PlayerService(db)
    return player_service.create(player_in)

@router.get("/{player_id}", response_model=Player)
def get_player(
    player_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Obter jogador por ID
    """
    player_service = PlayerService(db)
    player = player_service.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return player

@router.get("/", response_model=List[Player])
def list_players(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(deps.get_db)
):
    """
    Listar jogadores com paginação
    """
    player_service = PlayerService(db)
    return player_service.get_all(skip=skip, limit=limit, active_only=active_only)

@router.patch("/{player_id}", response_model=Player)
def update_player(
    player_id: int,
    player_in: PlayerUpdate,
    db: Session = Depends(deps.get_db)
):
    """
    Atualizar jogador
    """
    player_service = PlayerService(db)
    player = player_service.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return player_service.update(player, player_in)

@router.delete("/{player_id}", response_model=Player)
def delete_player(
    player_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Deletar jogador (soft delete)
    """
    player_service = PlayerService(db)
    player = player_service.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return player_service.soft_delete(player)

@router.post("/{player_id}/reactivate", response_model=Player)
def reactivate_player(
    player_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Reativar jogador
    """
    player_service = PlayerService(db)
    player = player_service.get_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return player_service.reactivate(player)