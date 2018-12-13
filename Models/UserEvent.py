from .Serializer import Serializer
from .ModelBase import Base
from sqlalchemy import (create_engine, Table, Column, Integer,
	String, DateTime, Float, MetaData, Boolean, ForeignKey)
from sqlalchemy.orm import relationship

class UserEvent(Base, Serializer):
	__tablename__ = "UserEvents"
	id = Column(Integer, primary_key=True)
	userId = Column(Integer, ForeignKey("Users.id"))
	user = relationship("User")
	eventId = Column(Integer, ForeignKey("Events.id"))
	event = relationship("Event")
	hidden = Column(Boolean)
	attended = Column(Boolean)
	points = Column(Integer)
	meta = Column(String)

	def serialize(self):
		d = Serializer.serialize(self)
		del d['user']
		return d

	def serialize_full(self):
		d = Serializer.serialize(self)
		del d['user']
		d['event'] = d['event'].serialize()
		return d