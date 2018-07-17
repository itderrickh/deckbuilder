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
    evolvesFrom = Column(String)
    hp = Column(Integer)
    retreatCost = Column(Integer)
    artist = Column(String)
    rarity = Column(String)
    types = Column(JSONType)
    attacks = Column(JSONType)
    weaknesses = Column(JSONType)
    evolvesTo = Column(JSONType)
    ability = Column(JSONType)
    setName = Column(String)
    setCode = Column(String)
    imageUrl = Column(String)
    localImageUrl = Column(String)
    type = Column(String)   #supertype
    number = Column(String)
    count = 0

    def serialize(self):
        d = Serializer.serialize(self)
        d['name'] = str(d['name'].decode("utf-8"))
        d['evolvesFrom'] = str(d['evolvesFrom'].decode("utf-8"))
        d['count'] = self.count
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        d['types'] = d['types'].serialize()
        d['attacks'] = d['attacks'].serialize()
        d['weaknesses'] = d['weaknesses'].serialize()
        d['evolvesTo'] = d['evolvesTo'].serialize()
        d['ability'] = d['ability'].serialize()
        d['count'] = self.count
        return d