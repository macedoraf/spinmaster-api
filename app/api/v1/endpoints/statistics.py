from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas import StatisticsResponse
from app.services import statistics_service

router = APIRouter()

@router.get("/player/{player_id}", response_model=StatisticsResponse)
def get_player_statistics(
    player_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get comprehensive statistics for a player"""
    return statistics_service.get_player_statistics(db=db, player_id=player_id)

@router.get("/global", response_model=StatisticsResponse)
def get_global_statistics(
    db: Session = Depends(deps.get_db)
):
    """Get global system statistics"""
    return statistics_service.get_global_statistics(db=db)
