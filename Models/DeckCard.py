from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer,
    String, MetaData, ForeignKey)
from sqlalchemy.orm import relationship

class DeckCard(Base, Serializer):
    __tablename__ = "DeckCards"
    id = Column(Integer, primary_key=True)
    deckId = Column(Integer, ForeignKey("Decks.id"))
    deck = relationship("Deck")
    cardId = Column(Integer, ForeignKey("Cards.Id"))
    card = relationship("Card")
    count = Column(Integer)

    def serialize(self):
        d = Serializer.serialize(self)
        del d["deck"]
        del d["card"]
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        d["card"] = d["card"].serialize()
        d["deck"] = d["deck"].serialize()
        return d