from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from app.db.session import engine

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # Adicione aqui outros atributos/métodos comuns para todos os modelos
    __allow_unmapped__ = True

Base = declarative_base(cls=CustomBase)

# Importar os modelos em ordem de dependência
from app.models.player import Player  # Tabela independente
from app.models.tournament import Tournament  # Tabela independente
# from app.models.tournament_player import TournamentPlayer  # Depende de Player e Tournament
from app.models.match import Match  # Depende de Player e Tournament
from app.models.set import Set  # Depende de Match
from app.models.ranking import Ranking  # Depende de Player

# Create tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)