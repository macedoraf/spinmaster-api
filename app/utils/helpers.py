from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
import math
from .constants import (
    INITIAL_RATING,
    K_FACTOR,
    MIN_RATING,
    MAX_RATING,
    PLAYER_CATEGORIES
)

def calculate_elo_rating(
    player_rating: float,
    opponent_rating: float,
    won: bool,
    k_factor: float = K_FACTOR
) -> float:
    """
    Calculate the new ELO rating for a player after a match.
    
    Args:
        player_rating (float): Current rating of the player
        opponent_rating (float): Current rating of the opponent
        won (bool): Whether the player won the match
        k_factor (float): K-factor for ELO calculation
        
    Returns:
        float: New rating for the player
    """
    expected_score = 1 / (1 + math.pow(10, (opponent_rating - player_rating) / 400))
    actual_score = 1.0 if won else 0.0
    new_rating = player_rating + k_factor * (actual_score - expected_score)
    
    return max(min(new_rating, MAX_RATING), MIN_RATING)

def get_player_category(rating: float) -> str:
    """
    Determine player's category based on their rating.
    
    Args:
        rating (float): Player's current rating
        
    Returns:
        str: Category name
    """
    for category, (min_rating, max_rating) in PLAYER_CATEGORIES.items():
        if min_rating <= rating <= max_rating:
            return category
    return 'beginner'

def calculate_win_percentage(wins: int, total_matches: int) -> float:
    """
    Calculate win percentage.
    
    Args:
        wins (int): Number of wins
        total_matches (int): Total number of matches
        
    Returns:
        float: Win percentage between 0 and 100
    """
    if total_matches == 0:
        return 0.0
    return round((wins / total_matches) * 100, 2)

def format_duration(start_time: datetime, end_time: datetime) -> str:
    """
    Format the duration between two timestamps.
    
    Args:
        start_time (datetime): Start timestamp
        end_time (datetime): End timestamp
        
    Returns:
        str: Formatted duration string
    """
    duration = end_time - start_time
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def paginate_results(
    items: List[Any],
    page: int,
    page_size: int
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Paginate a list of items.
    
    Args:
        items (List[Any]): List of items to paginate
        page (int): Page number
        page_size (int): Items per page
        
    Returns:
        Tuple[List[Any], Dict[str, Any]]: Paginated items and pagination metadata
    """
    total_items = len(items)
    total_pages = math.ceil(total_items / page_size)
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_items = items[start_idx:end_idx]
    
    pagination_meta = {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }
    
    return paginated_items, pagination_meta

def generate_tournament_brackets(
    players: List[str],
    seeded_players: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Generate tournament brackets based on number of players and seeds.
    
    Args:
        players (List[str]): List of player IDs
        seeded_players (Optional[List[str]]): List of seeded player IDs
        
    Returns:
        List[Dict[str, Any]]: Tournament bracket structure
    """
    num_players = len(players)
    bracket_size = 2 ** math.ceil(math.log2(num_players))
    byes = bracket_size - num_players
    
    # Initialize brackets
    brackets = []
    seeded_players = seeded_players or []
    unseeded_players = [p for p in players if p not in seeded_players]
    
    # Distribute seeds and byes optimally
    for i in range(bracket_size // 2):
        match = {
            "match_id": i + 1,
            "round": 1,
            "player1": None,
            "player2": None
        }
        
        # Add seeded players first
        if i < len(seeded_players):
            match["player1"] = seeded_players[i]
        elif unseeded_players:
            match["player1"] = unseeded_players.pop(0)
            
        # Add second player or bye
        if unseeded_players:
            match["player2"] = unseeded_players.pop(0)
            
        brackets.append(match)
    
    return brackets

def utc_now() -> datetime:
    """
    Get current UTC timestamp.
    
    Returns:
        datetime: Current UTC datetime
    """
    return datetime.now(timezone.utc)