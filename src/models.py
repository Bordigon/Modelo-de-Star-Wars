from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, session
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(280), unique = True, nullable = False)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    my_favourites: Mapped[List["Favourites"]] = relationship(back_populates = "user") 


    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "age":self.age,
            "email": self.email,
            "active":self.is_active
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(280), unique = True, nullable = False)
    age: Mapped[int] = mapped_column(nullable=False)
    films: Mapped[str] = mapped_column(String(280), unique = True, nullable = False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    characters_favourites: Mapped[List["Favourites"]] = relationship(back_populates = "character")

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "age":self.age,
            "films": self.films,
            "description":self.description
        }
    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(280), unique = True, nullable = False)
    age: Mapped[int] = mapped_column(nullable=False)
    galaxy: Mapped[str] = mapped_column(String(280), unique = True, nullable = False)
    self_conscious_especies: Mapped[str] = mapped_column(String(300), unique = True, nullable = False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    planets_favourites: Mapped[List["Favourites"]] = relationship(back_populates = "planet")

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "age":self.age,
            "galaxy":self.galaxy,
            "self_conscious_especies": self.self_conscious_especies,
            "description":self.description
        }
    
class Favourites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable = True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable = True)
    user: Mapped["User"] = relationship(back_populates="my_favourites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="characters_favourites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="planets_favourites")

    def serialize(self):
        return{
            "id":self.id,
            "user_id":self.user_id,
            "character_id":self.character_id,
            "planet_id":self.planet_id
        }
