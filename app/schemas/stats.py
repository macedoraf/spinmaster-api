from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class PlayerPerformance(BaseModel):
    total_matches: int
    wins: int
    losses: int
    win_rate: float
    average_points_per_match: float
    best_win: float
    worst_loss: float
    average_games_per_match: float

class HeadToHead(BaseModel):
    player_id: int
    opponent_id: int
    matches_played: int
    wins: int
    losses: int
    win_rate: float
    average_points_gained: float
    last_match_date: datetime
    winning_streak: int

class PerformanceByLevel(BaseModel):
    level: str
    matches_played: int
    wins: int
    losses: int
    win_rate: float
    average_points_gained: float

class TimeBasedStats(BaseModel):
    period: str  # e.g., "2024-01", "2024-Q1", "2024"
    matches_played: int
    win_rate: float
    average_rating: float
    rating_change: float
    tournament_participation: int
    tournament_wins: int

class ActivityStats(BaseModel):
    last_match_date: datetime
    matches_last_30_days: int
    tournaments_last_30_days: int
    active_days_streak: int
    longest_activity_streak: int

class SystemStats(BaseModel):
    total_players: int
    active_players: int
    total_matches: int
    matches_today: int
    matches_this_month: int
    ongoing_tournaments: int
    average_rating: float
    rating_distribution: Dict[str, int]  # rating range -> count
    level_distribution: Dict[str, int]  # level -> count
