from fastapi import APIRouter

from app.api.v1.endpoints import (
    players,
    matches,
    tournaments,
    rankings,
    # statistics
)

api_router = APIRouter()

# Include all endpoint routers with their prefixes
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(rankings.router, prefix="/rankings", tags=["rankings"])
# api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])