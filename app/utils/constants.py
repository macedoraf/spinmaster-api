# System-wide constants for the Table Tennis Ranking System

# Ranking Constants
INITIAL_RATING = 1000
K_FACTOR = 32  # Base K-factor for ELO calculation
MIN_RATING = 100
MAX_RATING = 3000

# Tournament Constants
MIN_PLAYERS_TOURNAMENT = 4
MAX_PLAYERS_TOURNAMENT = 64
TOURNAMENT_BONUS_MULTIPLIER = 1.5

# Match Constants
GAMES_TO_WIN = 3  # Best of 5
MIN_POINTS_TO_WIN = 11
MIN_POINT_DIFFERENCE = 2

# Player Categories
PLAYER_CATEGORIES = {
    'beginner': (0, 1200),
    'intermediate': (1201, 1800),
    'advanced': (1801, 2400),
    'elite': (2401, 3000)
}

# Cache Settings
CACHE_TTL = {
    'rankings': 3600,  # 1 hour
    'statistics': 1800,  # 30 minutes
    'player_profile': 300  # 5 minutes
}

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Rate Limiting
RATE_LIMIT_MATCHES = 50  # Maximum matches per player per day
RATE_LIMIT_API = {
    'anonymous': 100,  # requests per hour
    'authenticated': 1000  # requests per hour
}

# Achievement Thresholds
ACHIEVEMENTS = {
    'winning_streak': {
        'bronze': 5,
        'silver': 10,
        'gold': 20
    },
    'matches_played': {
        'bronze': 50,
        'silver': 100,
        'gold': 500
    },
    'tournaments_won': {
        'bronze': 1,
        'silver': 5,
        'gold': 10
    }
}