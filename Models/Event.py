from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer,
	String, DateTime, Float, MetaData, ForeignKey)
from sqlalchemy.orm import relationship

class Event(Base, Serializer):
	__tablename__ = "Events"
	id = Column(Integer, primary_key=True)
	title = Column(String)
	location = Column(String)
	status = Column(String)
	date = Column(DateTime)
	link = Column(String)

	def serialize(self):
		d = Serializer.serialize(self)
		return d

	def serialize_full(self):
		d = Serializer.serialize(self)
		return d