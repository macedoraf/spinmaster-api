from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.schemas.tournament import TournamentCreate, Tournament
from app.services.tournament_service import TournamentService

router = APIRouter()
tournament_service = TournamentService()

@router.post("/", response_model=Tournament)
def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(deps.get_db)
):
    """Create a new tournament"""
    return tournament_service.create_tournament(db=db, tournament=tournament)

@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(
    tournament_id: int = Path(..., title="The ID of the tournament to get"),
    db: Session = Depends(deps.get_db)
):
    """Get tournament by ID"""
    tournament = tournament_service.get_tournament(db=db, tournament_id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.get("/", response_model=List[Tournament])
def list_tournaments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    status: Optional[str] = Query(None, enum=["upcoming", "ongoing", "completed"]),
    db: Session = Depends(deps.get_db)
):
    """List tournaments with optional status filter"""
    return tournament_service.get_tournament(
        db=db, 
        skip=skip, 
        limit=limit, 
        status=status
    )
