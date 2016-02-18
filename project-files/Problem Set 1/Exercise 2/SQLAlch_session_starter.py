from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from DB_setup import *

engine = create_engine('sqlite:///app.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()