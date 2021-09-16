#!/usr/bin/env python3
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


class episodes(db.Model):# enumerations
    """ """
    __tablename__='Episodes'
    id=db.Column(db.Integer(),primary_key=True)
    season=db.Column(db.Integer())
    episode=db.Column(db.Integer())
    minor_ep=db.Column(db.Integer())
    ep_name=db.Column(db.String())

    def __init__(self,season,episode,minor,name):
        self.season=season
        self.episode=episode
        self.minor_ep=minor
        self.ep_name=name
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,dir(self),self.id)

class quotes(db.Model):#quote holder
    """ """
    __tablename__='Quotes'
    id=db.Column(db.Integer(),primary_key=True)
    ep_id=db.Column(db.Integer, db.ForeignKey('Episodes.id'),nullable=False)
    l_num=db.Column(db.Integer())
    character=db.Column(db.Integer, db.ForeignKey('Characters.id'),nullable=False)
    quote=db.Column(db.String())

    def __init__(self,ep_id,l_num,char,quote):
        self.name=
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,dir(self),self.id)

class characters(db.Model):# sorta enumeration, how do we handle multiple speakers?
    """ """
    __tablename__='Characters'
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),unique=True)

    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return '<{}:{} #{}>'.format(self.__tablename__,dir(self),self.id)

class query(db.Model):
    """ """
    __tablename__='Querys'
    id=db.Column(db.Integer(),primary_key=True)
    quote_id=db.Column(db.Integer(),db.ForeignKey('Quotes.id'),nullable=False)
    datetime=db.Column(db.DateTime())

    def __init__(self,name):
        self.name=name
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
                # using quote_finder as a cheeky parser
                import quote_finder as qf
                qf.populate_fake_database()
                for line in qf.Fake_Database:
                    # Parse into sqlalchemy models as defined above
                    # db.session.add(new object)
                    print(line)
                # db.session.commit()# commit objects to database
            elif arg=='peek':# peek at database entries
                print('peeking at db')
                # currently only characters added
                print((characters.query.all()))
    else:
        print('avaliable parameters: createdb, populatedb, peek')

if __name__=='__main__':
    main()
