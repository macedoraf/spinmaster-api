from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.schemas.ranking import RankingEntry
from app.services.ranking_service import RankingService

router = APIRouter()
ranking_service = RankingService()

@router.get("/current", response_model=List[RankingEntry])
def get_current_rankings(
    category: Optional[str] = Query(None, description="Filter by player category"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(deps.get_db)
):
    """Get current rankings, optionally filtered by category"""
    return ranking_service.get_player_history(
        db=db, 
        category=category, 
        limit=limit
    )

@router.get("/player/{player_id}/history", response_model=List[RankingEntry])
def get_player_ranking_history(
    player_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(deps.get_db)
):
    """Get ranking history for a specific player"""
    return ranking_service.get_player_history(
        db=db,
        player_id=player_id,
        start_date=start_date,
        end_date=end_date
    )
