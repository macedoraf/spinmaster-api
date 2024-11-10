# Import all the models, so that Base has them before being
# imported by Alembic
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import engine

Base = declarative_base()

# Import all models here
from app.models.player import Player
from app.models.match import Match
from app.models.tournament import Tournament
from app.models.ranking import Ranking

# Create tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)