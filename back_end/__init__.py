#Seak Yith
#Connecting flask

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from .quote_search import *
from .model import *
app = Flask(__name__)

# combine lists into a tuple
def merge(list1, list2, list3, list4):
    mergedList= tuple(zip(list1, list2, list3, list4))
    return mergedList


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
            
            # if query fails return to home page
            if not result:
                return render_template("home.html") 
            season = []
            episode = []
            character = []
            actualQuote = []
            for x in result:
                season.append(x.episode.season)
                episode.append(x.episode.episode)
                character.append(x.character.name)
                actualQuote.append(x.quote)
            
            data = merge(season, episode, character, actualQuote)

            return render_template('results.html', data = data)
        else:
            return render_template("home.html") 
    else:  ## get method 
        return render_template("home.html") 
