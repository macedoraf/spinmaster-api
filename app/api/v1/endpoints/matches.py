from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.match import Match, MatchCreate, MatchUpdate
from app.services.match_service import MatchService

router = APIRouter()

@router.post("/", response_model=Match)
def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova partida com seus sets
    """
    match_service = MatchService(db)
    return match_service.create_match(match_data)

@router.get("/{match_id}", response_model=Match)
def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna uma partida específica
    """
    match_service = MatchService(db)
    return match_service.get_match(match_id)

@router.get("/", response_model=List[Match])
def get_matches(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    player_id: Optional[int] = None,
    tournament_id: Optional[int] = None
):
    """
    Lista partidas com opção de filtros
    """
    match_service = MatchService(db)
    return match_service.get_matches(
        skip=skip,
        limit=limit,
        player_id=player_id,
        tournament_id=tournament_id
    )

@router.patch("/{match_id}", response_model=Match)
def update_match(
    match_id: int,
    match_update: MatchUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma partida
    """
    match_service = MatchService(db)
    return match_service.update_match(match_id, match_update)

@router.delete("/{match_id}")
def delete_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove uma partida e seus sets
    """
    match_service = MatchService(db)
    match_service.delete_match(match_id)
    return {"message": "Match successfully deleted"}