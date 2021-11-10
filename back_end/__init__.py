#Seak Yith
#Connecting flask

from flask import Flask, request, render_template
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from .functions import *
from flask_paginate import Pagination, get_page_args
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
def populate():
    populate_database()
    return redirect(url_for('quote_generator'))

@app.route('/home', methods=["GET","POST"])
def quote_generator():
    if request.method=="POST":# Catch Post Form
        query = request.form['query']
        if query:
            result = grab_all_quotes(query)
            
            # if query fails return to home page
            if not result:
                message = "Unable find the qoute. Please re-enter a word or phrase."
                return render_template("home.html", message = message, quote_of_the_day = get_qod())

            return redirect(url_for('result_page', query_final=query))
        else:
            return render_template("home.html", quote_of_the_day = get_qod()) 
    else:  ## get method 
        return render_template("home.html", quote_of_the_day = get_qod()) 

@app.route('/result/<query_final>')
def result_page(query_final):
    result = grab_all_quotes(query_final)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(result)
    paginate_datas = result[offset : offset + per_page]
    data_tuple = store_all_quotes(result, query_final)
    data_tuple = data_tuple[offset : offset + per_page]
    paginate = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('results.html', datas=paginate_datas, page=page, per_page=per_page, paginate=paginate, data_tuple=data_tuple, chr_img_paths=chr_img_paths)
