from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class CardSet(Base, Serializer):
    __tablename__ = "CardSet"
    Id = Column(Integer, primary_key=True)
    name = Column(String)
    setName = Column(String)
    standard = Column(Boolean)
    shortName = Column(String)
    fileName = Column(String)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def serialize_full(self):
        d = Serializer.serialize(self)
        return d