"""
# Authors:
# -shazelquist
# 
# Directives:
# -Provide a basic schema for a sql database
"""
# Authors
# -shazelquist

# Notes:
# -Full linting style and document not provided

#
# Imports:
from sys import argv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Directive:
# -Generate hypothetical schemea for db
# Notes:
# -DB access should not run from this file
# -This is not a finalized version
# -No methods declared
# -May require {context, desciptions, groups, etc...}

if 'app' not in dir():# set the app if run alone (not actually sure if this works)
    app=Flask(__name__)

# configurations
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False# remove tracking overhead
# set the name and path to the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3_Sponge_Who.db'
db=SQLAlchemy(app)


class episodes(db.Model):# Stores information regarding episodes
    """SQLAchemy model episodes"""
    __tablename__='Episodes'
    id=db.Column(db.Integer(),primary_key=True)
    season=db.Column(db.Integer())
    episode=db.Column(db.Integer())
    minor_ep=db.Column(db.Integer())
    ep_name=db.Column(db.String())
    ep_des=db.Column(db.String())

    def __init__(self,season,episode,minor,name,description):
        """Initialization for "episodes" sqlobject, requires(season:int,episode:int,minor:int,name:str,description:str)"""
        self.season=season
        self.episode=episode
        self.minor_ep=minor
        self.ep_name=name
        self.ep_des=description
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,(self.season,self.episode,self.minor_ep,self.ep_name,self.ep_des),self.id)

class quotes(db.Model):# Stores information regarding character quotes
    """SQLAlchemy model quotes"""
    __tablename__='Quotes'
    id=db.Column(db.Integer(),primary_key=True)
    ep_id=db.Column(db.Integer, db.ForeignKey('Episodes.id'),nullable=False)
    l_num=db.Column(db.Integer())
    char_id=db.Column(db.Integer, db.ForeignKey('Characters.id'),nullable=False)
    quote=db.Column(db.String())

    episode=db.relationship("episodes",foreign_keys=[ep_id])
    character=db.relationship("characters",foreign_keys=[char_id])
    def __init__(self,ep_id:int,l_num:int,character:int,quote:str):
        """Initialization for "quotes" sqlobject, requires(ep_id:int,l_num:int,character:int,quote:str)"""
        self.ep_id=ep_id
        self.l_num=l_num
        self.char_id=character
        self.quote=quote
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,(self.l_num,self.char_id,self.quote),self.id)

class characters(db.Model):# Stores information for characters, may require pseudoname parsing
    """SQLAchemy model characters"""
    __tablename__='Characters'
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),unique=True)

    def __init__(self,name:str):
        """Initialization for "characters" sqlobject, requires(character name:str)"""
        self.name=name
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,self.name,self.id)

# The following models are experimental
class user_query(db.Model):
    """User_query"""# store information regarding queries and user feedback?
    __tablename__='User_querys'
    id=db.Column(db.Integer(),primary_key=True)
    query_text=db.Column(db.String())
    quote_id=db.Column(db.Integer(),db.ForeignKey('Quotes.id'),nullable=False)
    datetime=db.Column(db.DateTime())
    accurate=db.Column(db.Boolean())

    def __init__(self):
        """Initialization for "user_query" sqlobject"""
        pass
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,self.name,self.id)

def main():
    """Main function"""
    # running as standalone function for debugging, provides some basic options
    if len(argv):

        for arg in argv[1:]:
            if arg=='createdb':
                print('creating database')
                db.create_all()#create schemea
                print('db should be created')
            elif arg=='populatedb':
                print('populating database')
                # using quote_search as a cheeky parser
                print('populating database')
                mc=characters('spongebob')
                print(mc)
                db.session.add(mc)
                db.session.commit()
                print(mc)
                ep=episodes(1,1,1,'epname','desc')
                print(ep)
                db.session.add(ep)
                db.session.commit()
                print(ep)
                print(ep.id,mc.id)
                q=quotes(ep.id,15,mc.id,'the user quote')
                print(q)
                db.session.add(q)
                db.session.commit()
                print(q)
                print(q.character,q.episode)
            elif arg=='peek':# peek at database entries
                print('peeking at db')
                # currently only characters added
                print((characters.query.all()))
                print((episodes.query.all()))
                print((quotes.query.all()))
                print(quotes.query.all()[0].episode)
    else:
        print('avaliable parameters: createdb, populatedb, peek')

if __name__=='__main__':
    main()
