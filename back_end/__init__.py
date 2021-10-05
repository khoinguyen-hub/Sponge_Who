#Seak Yith
#Connecting flask

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from back_end.quote_search import *
from back_end.model import *
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
            ### need to run these code on the first set up
            # db.create_all()
            # dict = parseTextFile()
            # newdict = cleanDict(dict)
            # populateDatabaseCharacters(newdict)
            # populateDatabaseQuotes(newdict)
            ###
            result = quotes.query.filter(quotes.quote.contains(query)).all()
            character = characters.query.filter_by(name = query).first()
            print("The qoute is " + str(result[0].quote))
            print("The Character is " + str(result[0].character.name))
            # for x in result:
            #     #print(str(x.character.name) + ": " + x.quote)
            #     print((characters.query.all()))
            #     print((episodes.query.all()))
            return render_template('results.html')## might need to change html name
        else:
            return render_template("home.html") 
    else:  ## get method 
        return render_template("home.html") 