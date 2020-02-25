from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData, ForeignKey)
from sqlalchemy.orm import relationship

class Deck(Base, Serializer):
    __tablename__ = "Decks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sprites = Column(String)
    userId = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")

    def serialize(self):
        d = Serializer.serialize(self)
        d['sprites'] = d['sprites'].split(';')
        del d['user']
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        d['user'] = d['user'].serialize()
        d['sprites'] = d['sprites'].split(';')
        return d