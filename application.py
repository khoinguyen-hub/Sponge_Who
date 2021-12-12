#Seak Yith
#Khoi Nguyen
#Daiwei Chen
#Shane Hazelquist
#Connecting flask
#Adding RestAPI

from flask import Flask, request, render_template, Response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from functions import *
from flask_paginate import Pagination, get_page_args
# importing flask_restful 
from flask_restful import Resource, Api, reqparse, abort
from sqlalchemy import desc, and_
from random import randrange
import json

app = Flask(__name__)
# adding API
api = Api(app)

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
            filterCharacters = request.form.getlist("characterCheckBox")
            result = grab_all_quotes(query)
            
            # if query fails return to home page
            if not result:
                message = "Unable to find the qoute. Please re-enter a word or phrase."
                return render_template("home.html", message = message, quote_of_the_day = get_qod())
            if not filterCharacters:
                return redirect(url_for('result_page', query_final=query))
            else:
                return redirect(url_for('result_pageWithFilter', query_final=query, characterList = filterCharacters))
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
    audio_generator(paginate_datas)
    songs = os.listdir('static/sounds/')
    return render_template('results.html', datas=paginate_datas, page=page, per_page=per_page, paginate=paginate, data_tuple=data_tuple, chr_img_paths=chr_img_paths, songs=songs)

# API doc route
@app.route('/api_documentation',methods=["GET"])
def documentation_page():
    """ method for serving readable documentation"""
    # load api_doc.txt and pass to template
    with open('static/api_doc.json') as doc_dataf:
        return  render_template('API_home.html', api_doc=json.load(doc_dataf))
    return Response(status=500)

@app.route('/result/<query_final>/<characterList>')
def result_pageWithFilter(query_final, characterList):
    print("second result page")
    # result = []
    # for character in characterList:
    #     tempresult = (quoteByCharacter(character))
    #     result.append(tempresult)
    print(characterList)
    print("size", len(characterList))
    result = quoteByCharacter(characterList, query_final)
    if not result:
        message = "Unable to find the qoute. Please re-enter a word or phrase or re-select characters"
        return render_template("home.html", message = message, quote_of_the_day = get_qod())

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(result)
    paginate_datas = result[offset : offset + per_page]
    data_tuple = store_all_quotes(result, query_final)
    data_tuple = data_tuple[offset : offset + per_page]
    paginate = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    audio_generator(paginate_datas)
    songs = os.listdir('static/sounds/')
    return render_template('results.html', datas=paginate_datas, page=page, per_page=per_page, paginate=paginate, data_tuple=data_tuple, chr_img_paths=chr_img_paths, songs=songs)

# API classes
class HomeEndPoint(Resource):
    def get(self):
        return {'data':'Welcome to HomePage'}

class api_query(Resource):
    """Method for serving the api"""
    def put(self):
        """method for serving queries"""
        try:
            query=request.form['query']
            res=db.session.query(query).all()
            db.session.rollback()
            return {'query':'SELECT '+query,'queryresult':res}
        except:
            return Response(response="Bad_query:'SELECT {}'".format(query),status=400)

class api_popular(Resource):# qod on get
    """api object for serving quotes based on popularity"""
    def put(self):
        """Serve N most popular quotes"""
        try:
            count=int(request.form['count'])
            ids=[s[0] for s in db.session.query(quote_logging.id).order_by(desc(quote_logging.searches)).limit(count).all()]
            return [{'character':q.character.name,'quote_id':q.id,'quote':q.quote} for q in db.session.query(quotes).filter(quotes.id.in_(ids)).all()]
        except:
            return Response(response="Bad_query",status=400)
    def get(self):
        """Serves quote of the day as most popular quote"""
        return [get_qod()]

class api_script(Resource):
    """api object for serving scripts of episodes"""
    def put(self):
        """Serve script given episode number information"""
        try:
            season=int(request.form['season'])
            episode=int(request.form['episode'])
            minor=int(request.form['minor'])
            ids=db.session.query(episodes.id).filter(episodes.season==season).filter(episodes.episode==episode).filter(episodes.minor_ep==minor).first()[0]
            qs=db.session.query(characters.name,quotes.quote).filter(quotes.ep_id==ids).filter(characters.id==quotes.char_id).all()#
            return qs
        except:
            return Response(response="Bad_query",status=400)

class api_sponge_who(Resource):
    """api object for serving sponge who functionality"""
    def put(self):
        """Serve quote information from quote guess"""
        try:
            subquote=request.form['quote_guess']
            result=grab_all_quotes(subquote)
            if not result:
                return [None]
            return [{'season':q.episode.season,'episode':q.episode.episode,'minor':q.episode.minor_ep,'character':q.character.name,'quote_id':q.id,'quote':q.quote} for q in result]
        except:
            return Response(response="Bad_query:'SELECT {}'".format(query),status=400)

class api_random(Resource):
    """api object for serving random quote"""
    def get(self):
        """randomly selects a quote from static range"""
        return {'quote':db.session.query(quotes.quote).filter(quotes.id==randrange(1,54178)).first()[0]}

class api_voiceline(Resource):
    """api object for serving tts quotes""" #currently broken, figuring out how to send file
    def put(self):
        """Serve tts quotes"""
        #try:
        # guess, voicelines out
        qid=int(request.form['quote_id'])
        res=db.session.query(quotes.quote).filter(quotes.id==qid).first()
        voice=gTTS(res, lang='en')
        voice.save('api_req_')
        return #[q.quote for q in res]
        #except:
        #    return Response(response="Bad_query:'SELECT {}'".format(query),status=400)

api.add_resource(HomeEndPoint, '/WelcomeToHomePage')
api.add_resource(api_query,'/api_query')
api.add_resource(api_popular,'/api_popular')
api.add_resource(api_script,'/api_script')
api.add_resource(api_random,'/api_random')
api.add_resource(api_sponge_who,'/api_sponge_who')

if __name__ == '__main__':
    app.run(debug=True)
