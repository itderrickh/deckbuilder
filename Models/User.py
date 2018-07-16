from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer,
    String, MetaData, ForeignKey, Date)
import datetime

class User(Base, Serializer):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    playerid = Column(String)
    dateofbirth = Column(Date)
    theme = Column(String)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d