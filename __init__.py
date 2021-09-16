#!/usr/bin/env python3
"""
# Authors:
# -shazelquist
# 
# Directive:
# Generate a simple quote lookup and print the results via a flask web application
# Notes:
# -don't forget to (activate virtualenv?) and set enviornment variables for flask
# -once env variables are set use flask run
# -given template satisfies all html requests so far
"""
#
# Authors:
# -shazeqluist
#
# Imports:
from flask import Flask, request, render_template# Flask directives
from .quote_finder import searchstring, populate_fake_database# Fake DB operations

print(__name__)
app = Flask(__name__)#set flask app name
populate_fake_database()# populate fake database from textfile

@app.route('/', methods=["GET","POST"])# this route handles both get & post
def quote_finder():
    "Recieves requests, queries if POST method"
    if request.method=="POST":# Catch Post Form
        query=request.form['query']# Retrieve query value from form
        if query:# if Non-empty query
            results=searchstring(query)# search query in fake database
            #Given results, render template and fill in infomation
            # Query:"" Number of result(s):
            # -each result
            return render_template('home.html',message="query:\"{}\" {} result{}:".format(query,len(results),
            's'*(len(results)>1)),query_results=results)
        else:
            return render_template('home.html',message="No query detected",query_results='')
    elif request.method=="GET":# Get request, Assume this is the first visit so tell them what to do
        return render_template('home.html',message="Please search for a quote ",query_results='')
    else:
        print('Unknown method, please try again')
