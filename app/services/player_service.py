from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.core.security import get_password_hash
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate

class PlayerService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, player_id: int) -> Optional[Player]:
        return self.db.query(Player).filter(Player.id == player_id).first()

    def get_by_email(self, email: str) -> Optional[Player]:
        return self.db.query(Player).filter(Player.email == email).first()

    def get_by_username(self, username: str) -> Optional[Player]:
        return self.db.query(Player).filter(Player.username == username).first()

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> List[Player]:
        query = self.db.query(Player)
        if active_only:
            query = query.filter(Player.is_active == True)
        return query.offset(skip).limit(limit).all()

    def create(self, player_create: PlayerCreate) -> Player:
        # Verificar se já existe usuário com mesmo email
        if self.get_by_email(email=player_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Verificar se já existe usuário com mesmo username
        if self.get_by_username(username=player_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Criar o player
        player = Player(
            username=player_create.username,
            email=player_create.email,
            full_name=player_create.full_name,
            hashed_password=get_password_hash(player_create.password)
        )
        
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def update(self, player: Player, player_update: PlayerUpdate) -> Player:
        update_data = player_update.model_dump(exclude_unset=True)
        
        # Verificar email único se estiver sendo atualizado
        if "email" in update_data and update_data["email"] != player.email:
            if self.get_by_email(email=update_data["email"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
        if "avatar_url" in update_data:
            update_data["avatar_url"] = str(update_data["avatar_url"]) if update_data["avatar_url"] else None


        # Atualizar os campos
        for field, value in update_data.items():
            setattr(player, field, value)

        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        
        return player

    def delete(self, player: Player) -> Player:
        self.db.delete(player)
        self.db.commit()
        return player

    def soft_delete(self, player: Player) -> Player:
        player.is_active = False
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player

    def reactivate(self, player: Player) -> Player:
        player.is_active = True
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player

    def update_last_login(self, player: Player) -> Player:
        player.last_login = datetime.now()
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player