from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer, 
    String, MetaData, ForeignKey)

class User(Base, Serializer):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d