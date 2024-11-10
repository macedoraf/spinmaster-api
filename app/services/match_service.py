from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.match import Match
from app.models.set import Set
from app.schemas.match import MatchCreate, MatchUpdate

class MatchService:
    def __init__(self, db: Session):
        self.db = db
    
    def determine_winner(self, sets: List[Set], player1_id: int, player2_id: int) -> int:
        """Determina o vencedor baseado nos sets"""
        sets_won_p1 = sum(1 for set_data in sets if set_data.score_p1 > set_data.score_p2)
        sets_won_p2 = sum(1 for set_data in sets if set_data.score_p2 > set_data.score_p1)
        
        return player1_id if sets_won_p1 > sets_won_p2 else player2_id

    def create_match(self, match_data: MatchCreate) -> Match:
        try:
            winner_id = self.determine_winner(match_data.sets, match_data.player1_id, match_data.player2_id)
            
            match = Match(
                player1_id=match_data.player1_id,
                player2_id=match_data.player2_id,
                tournament_id=match_data.tournament_id,
                winner_id=winner_id
            )
            
            self.db.add(match)
            self.db.flush()
            
            # Create sets
            sets = [
                Set(
                    match_id=match.id,
                    set_number=set_data.set_number,
                    score_p1=set_data.score_p1,
                    score_p2=set_data.score_p2
                )
                for set_data in match_data.sets
            ]
            
            self.db.add_all(sets)
            self.db.commit()
            self.db.refresh(match)
            
            return match
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def get_match(self, match_id: int) -> Optional[Match]:
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        return match

    def get_matches(
        self, 
        skip: int = 0, 
        limit: int = 100,
        player_id: Optional[int] = None,
        tournament_id: Optional[int] = None
    ) -> List[Match]:
        query = self.db.query(Match)
        
        if player_id:
            query = query.filter(
                (Match.player1_id == player_id) | (Match.player2_id == player_id)
            )
            
        if tournament_id:
            query = query.filter(Match.tournament_id == tournament_id)
            
        return query.offset(skip).limit(limit).all()

    def update_match(
        self,
        match_id: int,
        match_update: MatchUpdate
    ) -> Match:
        match = self.get_match(match_id)
        
        if match_update.tournament_id is not None:
            match.tournament_id = match_update.tournament_id
            match.updated_at = datetime.now()
            
        try:
            self.db.commit()
            self.db.refresh(match)
            return match
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    
    def delete_match(self, match_id: int) -> None:
        match = self.get_match(match_id)
        
        try:
            # Deleta os sets primeiro devido à chave estrangeira
            self.db.query(Set).filter(Set.match_id == match_id).delete()
            self.db.delete(match)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
