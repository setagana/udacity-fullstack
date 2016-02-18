import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
	"""Class representing the restaurant DB table"""
	__tablename__ = 'shelter'
	
	name = Column(String(80), nullable = False)
	address = Column(String(120), nullable = False)
	city = Column(String(80), nullable = False)
	state = Column(String(80), nullable = False)
	zipCode = Column(Integer)
	website = Column(String(120))
	id = Column(Integer, primary_key = True)


class Puppy(Base):
	"""Class representing the menu item DB table"""
	__tablename__ = 'puppy'
	
	name = Column(String(80), nullable = False)
	date_of_birth = Column(Date)
	gender = Column(String(10))
	weight = Column(Float)
	id = Column(Integer, primary_key = True)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)