from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas import MatchCreate, MatchResponse
from app.services import match_service

router = APIRouter()

@router.post("/", response_model=MatchResponse)
def create_match(
    match: MatchCreate,
    db: Session = Depends(deps.get_db)
):
    """Record a new match"""
    return match_service.create_match(db=db, match=match)

@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int = Path(..., title="The ID of the match to get"),
    db: Session = Depends(deps.get_db)
):
    """Get match by ID"""
    match = match_service.get_match(db=db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.get("/player/{player_id}", response_model=List[MatchResponse])
def get_player_matches(
    player_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(deps.get_db)
):
    """Get matches for a specific player"""
    return match_service.get_player_matches(
        db=db, 
        player_id=player_id, 
        skip=skip, 
        limit=limit
    )
