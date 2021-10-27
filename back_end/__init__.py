#Seak Yith
#Connecting flask

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from .quote_search import *
from .model import *
app = Flask(__name__)

print(__name__)
#connecting to sql database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False# remove tracking overhead
# set the name and path to the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3_Sponge_Who.db'
db=SQLAlchemy(app)

@app.route('/', methods=["GET","POST"])
@app.route('/home', methods=["GET","POST"])
def quote_generator():
    if request.method=="POST":# Catch Post Form
        query = request.form['query']
        if query:
            result = quotes.query.filter(quotes.quote.contains(query)).all()

          
            for x in result:
                season = x.episode.season
                episode = x.episode.episode
                character = x.character.name
                actualQuote = x.quote
                print(f'season {season}; episode {episode}; character {character}; quote {actualQuote}')

            return render_template('results.html', season = season, episode = episode, line = actualQuote, result = result)
        else:
            return render_template("home.html") 
    else:  ## get method 
        return render_template("home.html") 
