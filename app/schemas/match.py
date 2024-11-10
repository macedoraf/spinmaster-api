from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, validator, model_validator

class MatchType(str, Enum):
    FRIENDLY = "friendly"
    TOURNAMENT = "tournament"
    CHALLENGE = "challenge"

class GameScore(BaseModel):
    player_score: int = Field(..., ge=0, le=11)
    opponent_score: int = Field(..., ge=0, le=11)

    @validator('player_score', 'opponent_score')
    def validate_score(cls, v):
        if not (0 <= v <= 11):
            raise ValueError('Score must be between 0 and 11')
        return v
    
    @model_validator(mode='after')
    def validate_game_winner(self):
        # Validar se há um vencedor claro (diferença de 2 pontos e alguém chegou a 11)
        if max(self.player_score, self.opponent_score) >= 11:
            if abs(self.player_score - self.opponent_score) < 2:
                raise ValueError('Game must be won by 2 points when score reaches 11')
        return self

class MatchCreate(BaseModel):
    match_type: MatchType = Field(..., description="Type of match: friendly, tournament, or challenge")
    player_id: int = Field(..., gt=0)
    opponent_id: int = Field(..., gt=0)
    tournament_id: Optional[int] = Field(None, gt=0)
    games: List[GameScore] = Field(..., min_items=3, max_items=5)
    notes: Optional[str] = Field(None, max_length=1000)

    @validator('opponent_id')
    def validate_different_players(cls, v, values):
        if 'player_id' in values and v == values['player_id']:
            raise ValueError('Player and opponent must be different')
        return v

    @validator('tournament_id')
    def validate_tournament_id(cls, v, values):
        if v is not None and values.get('match_type') != MatchType.TOURNAMENT:
            raise ValueError('Tournament ID should only be provided for tournament matches')
        if values.get('match_type') == MatchType.TOURNAMENT and v is None:
            raise ValueError('Tournament ID is required for tournament matches')
        return v

    @model_validator(mode='after')
    def validate_match_rules(self):
        # Contar vitórias
        player_wins = sum(1 for game in self.games if game.player_score > game.opponent_score)
        opponent_wins = sum(1 for game in self.games if game.opponent_score > game.player_score)
        
        # Verificar se o número de games é válido
        total_games = len(self.games)
        if not (3 <= total_games <= 5):
            raise ValueError('Match must have between 3 and 5 games')
        
        # Verificar se há um vencedor válido (melhor de 5)
        max_wins_needed = 3
        if player_wins != max_wins_needed and opponent_wins != max_wins_needed:
            raise ValueError(f'Match must have exactly {max_wins_needed} wins for one player')

        # Verificar se não há games extras após alguém vencer
        if player_wins > max_wins_needed or opponent_wins > max_wins_needed:
            raise ValueError('Match should end when a player reaches 3 wins')

        return self

    class Config:
        json_schema_extra = {
            "example": {
                "match_type": "tournament",
                "player_id": 1,
                "opponent_id": 2,
                "tournament_id": 1,
                "games": [
                    {"player_score": 11, "opponent_score": 9},
                    {"player_score": 11, "opponent_score": 7},
                    {"player_score": 9, "opponent_score": 11},
                    {"player_score": 11, "opponent_score": 8}
                ],
                "notes": "Great match with intense rallies"
            }
        }

class MatchResponse(BaseModel):
    """Response schema for match creation"""
    match_id: int
    status: str = "success"
    message: str = "Match created successfully"
    rating_changes: dict = Field(
        ...,
        description="Rating changes for both players",
        example={
            "player": {"previous": 1000.0, "new": 1015.5, "change": 15.5},
            "opponent": {"previous": 1000.0, "new": 984.5, "change": -15.5}
        }
    )