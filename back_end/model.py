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
# -Now requires sqlalchemy db URI from environment variable 'SQLALCHEMY_DATABASE_URI'

# Imports:
from sys import argv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime


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
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False# remove tracking overhead
# set the name and path to the database
#app.config['SQLALCHEMY_DATABASE_URI']=environ['SQLALCHEMY_DATABASE_URI']# may autoset
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3_Sponge_Who.db'
db=SQLAlchemy(app)


class episodes(db.Model):# Stores information regarding episodes
    """SQLAchemy model episodes"""
    __tablename__='Episodes'
    id=db.Column(db.Integer(),primary_key=True)
    season=db.Column(db.Integer())
    episode=db.Column(db.Integer())
    minor_ep=db.Column(db.Integer())
    ep_name=db.Column(db.String(),unique=True)# unique check
    ep_filename=db.Column(db.String())

    def __init__(self,season,episode,minor,name,filename):
        """Initialization for "episodes" sqlobject, requires(season:int,episode:int,minor:int,name:str,filename:str)"""
        self.season=season
        self.episode=episode
        self.minor_ep=minor
        self.ep_name=name
        self.ep_filename=filename
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,(self.season,self.episode,self.minor_ep,self.ep_name,self.ep_filename),self.id)

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
    logging=db.relationship("quote_logging", backref='quotes',primaryjoin="quotes.id == quote_logging.id")
    def __init__(self,ep_id:int,l_num:int,character:int,quote:str):
        """Initialization for "quotes" sqlobject, requires(ep_id:int,l_num:int,character:int,quote:str)"""
        self.ep_id=ep_id
        self.l_num=l_num
        self.char_id=character
        self.quote=quote
    def __repr__(self):
        return '<{}:{} Log:{} #{}>'.format(self.__tablename__,(self.l_num,self.char_id,self.quote),self.logging,self.id)

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

class quote_logging(db.Model):
    """quote_logging"""
    __tablename__='Quote_logging'
    id=db.Column(db.Integer(), db.ForeignKey('Quotes.id'),primary_key=True,nullable=False)
    searches=db.Column(db.Integer)
    last_call=db.Column(db.DateTime)

    def __init__(self, quote_id, start_num=1):
        """Initialization for "quote_logging" sqlobject, requires(quote.id), optional start_num for initial count"""
        self.id=quote_id
        self.searches=start_num
        if not self.searches:# don't push time if generic start
            self.last_call=datetime.now()
    def __repr__(self):
        return '<{}: searches:{} {} #{}>'.format(self.__tablename__,self.searches,self.last_call,self.id)

    def inc(self):
        """Increments quote logging"""
        self.searches+=1
        self.last_call=datetime.now()
    def get_last_call(self):# might implement str conversion
        """Returns timedate of last query"""
        return self.last_call
    def time_since_last_call(self):
        """Returns timedate.delta of last query"""
        return datetime.now()-self.last_call
    def get_searches(self):
        """Returns number of searches"""
        return self.searches

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
            elif arg=='populatelog':
                print('populating logging')
                allquotes=quotes.query.all()
                qlogs=[]
                for q in allquotes:
                    #print(q)
                    qlogs.append(quote_logging(q.id,start_num=0))
                db.session.add_all(qlogs)
                db.session.commit()

            elif arg=='peek':# peek at database entries
                print('peeking at db')
                # currently only characters added
                #print((characters.query.all()))
                print('episodes {}'.format(len(episodes.query.all())))
                print('Quotes:{} first ten:{}'.format(len(quotes.query.all()),(quotes.query.all()[:10])))
                print(quotes.query.all()[0].episode)
                print('number of logs {}'.format(len(quote_logging.query.all())))
    else:
        print('avaliable parameters: createdb, populatelog, peek')

if __name__=='__main__':
    main()
