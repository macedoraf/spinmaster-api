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
from app.models.player import Player
from app.models.match import Match 
from app.models.set import Set 

# Create tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)