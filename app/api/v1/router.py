from fastapi import APIRouter

from app.api.v1.endpoints import (
    players,
    matches
)

api_router = APIRouter()

# Include all endpoint routers with their prefixes
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])