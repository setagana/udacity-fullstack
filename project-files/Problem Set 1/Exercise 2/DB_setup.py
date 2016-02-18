import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
	"""Class representing the shelter DB table"""
	__tablename__ = 'shelter'
	
	name = Column(String(80), nullable = False)
	address = Column(String(120), nullable = False)
	city = Column(String(80), nullable = False)
	state = Column(String(80), nullable = False)
	zipCode = Column(Integer)
	website = Column(String(120))
	id = Column(Integer, primary_key = True)


class Puppy(Base):
	"""Class representing the puppy DB table"""
	__tablename__ = 'puppy'
	
	name = Column(String(80), nullable = False)
	date_of_birth = Column(Date)
	gender = Column(String(10))
	weight = Column(Float)
	id = Column(Integer, primary_key = True)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	puppy_profile = relationship("Puppy_Profile", uselist=False, back_populates="puppy")

class Puppy_Profile(Base):
	"""Class representing the puppy profile DB table"""
	__tablename__ = 'puppy_profile'
	id = Column(Integer, primary_key = True)
	puppy_id = Column(Integer, ForeignKey('puppy.id'))
	puppy = relationship("Puppy", back_populates="puppy_profile")
	photo = Column(String(120))
	description = Column(String(200))
	special_needs = Column(String(200))
		

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)