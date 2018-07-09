from .Serializer import Serializer
from .ModelBase import Base, JSONType
from sqlalchemy import (create_engine, Table, Column, Integer,
    String, MetaData, ForeignKey, JSON)
from sqlalchemy.orm import relationship

class Card(Base, Serializer):
    __tablename__ = "Cards"
    Id = Column(Integer, primary_key=True)
    name = Column(String)
    subtype = Column(String)
    hp = Column(Integer)
    retreatCost = Column(Integer)
    artist = Column(String)
    rarity = Column(String)
    types = Column(JSONType)
    attacks = Column(JSONType)
    weaknesses = Column(JSONType)
    evolvesTo = Column(JSONType)
    setName = Column(String)
    type = Column(String)   #supertype
    number = Column(String)

    def __init__(self):
       self.count = 0

    def serialize(self):
        d = Serializer.serialize(self)
        del d['deck']
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        d['deck'] = d['deck'].serialize()
        return d