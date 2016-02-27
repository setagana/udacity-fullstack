import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	"""Class representing the restaurant DB table"""
	__tablename__ = 'restaurant'
	
	name = Column(String(200), nullable = False)
	address = Column(String(200), nullable = False)
	city = Column(String(200), nullable = False)
	postcode = Column(String(200), nullable = False)
	phone = Column(String(200), nullable = False)
	website = Column(String(200), nullable = True)
	id = Column(Integer, primary_key = True)

	@property
	def serialize(self):
		return {
    		'name'	:	self.name,
    		'address'	:	self.address,
    		'city'	:	self.city,
    		'postcode'	:	self.postcode,
    		'phone'	:	self.phone,
    		'website'	:	self.website,
    	}

class MenuItem(Base):
	"""Class representing the menu item DB table"""
	__tablename__ = 'menu_item'
	
	name = Column(String(200), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(200), nullable = False)
	description = Column(String(200))
	price = Column(Integer, nullable = False)
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		return {
    		'name'	:	self.name,
    		'description'	:	self.description,
    		'id'	:	self.id,
    		'price'	:	self.price,
    		'course'	:	self.course,
    	}

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)