from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData, ForeignKey)
from sqlalchemy.orm import relationship

class Card(Base, Serializer):
    __tablename__ = "Cards"
    Id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer)
    setName = Column(String)
    type = Column(String)
    number = Column(String)
    deckId = Column(Integer, ForeignKey("Decks.id"))
    deck = relationship("Deck")

    def serialize(self):
        d = Serializer.serialize(self)
        del d['deck']
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        d['deck'] = d['deck'].serialize()
        return d