# Dawei Chen
# local database creation
# databse schema design

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Episode(Base):
	__tablename__ = 'Episode'

	id = Column(Integer(), primary_key = True)
	season = Column(String(99))
	episode_number = Column(String(99))
	minor_episode_num = Column(String(99))
	description = Column(String(99))

class Quote(Base):
	__tablename__ ='Quotes'

	id = Column(Integer(), primary_key = True)
	episode = Column(String(99))
	quote = Column(String(99))
	character = Column(String(99))
	line_number = Column(String(99))

class Character(Base):
	__tablename__ ='Character'

	id = Column(Integer(), primary_key = True)
	name = Column(String(99))
	
class Character(Base):
	__tablename__ ='Famouse_Quotes'

	famouse_quotes_id = Column(Integer(), primary_key = True)
	quote = Column(String(99))
	
class Icons(Base):
	__tablename__ ='Icons'

	icon_name = Column(String(99), primary_key = True)
	icon = Column(BLOB)

if __name__ =="__main__":
	engine = create_engine('sqlite:///PDB.db')
	Base.metadata.create_all(bind = engine)
