from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


#connecting to sql database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite3_Sponge_Who.db'
db = SQLAlchemy(app)

from . import routes