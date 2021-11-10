# Created by Khoi Nguyen
# This file contains functions for use from flask view to reduce 
# cluster in the view

from os.path import exists as file_exists
from .quote_search import *
from sqlalchemy import func

# Current Quote of the day
qod=None
# Character image paths
chr_img_paths={"SpongeBob":"spongebobwindowspb.png","Patrick":"patrickwindowspb.png","Sandy":"sandywindowspb.png","Mr. Krabs":"mrkrabswindowspb.png"}

#populate database if it doesn not exists
def populate_database():
    if file_exists('sqlite3_Sponge_Who.db'):
        print('Database already exists')
    else:
        db.create_all()
        dict = parseTextFile()
        newdict = cleanDict(dict)
        populateDatabaseCharacters(newdict)
        populateDatabaseQuotes(newdict)

# Shane Hazelquist
# Get the quote of the day, and update if stale
def get_qod():
    """returns quote of the day and updates stale qod"""
    global qod
    if not qod or qod.logging[0].time_since_last_call().days>=1:
        res=db.session.query(quote_logging,func.max(quote_logging.searches)).first()[0]
        qod=quotes.query.filter(quotes.id==res.id).first()
        print('Updated Quote of the day:"{}"'.format(qod))
    return qod.quote

# Shane Hazelquist
# Seperate quote into tuple for highlighting
def highlight(query,quote):
    """Seperate quote into tuple for highlighting"""
    startindex=quote.lower().find(query.lower())
    if startindex==-1:# exception, don't index to -1
        return (quote,'','')
    endindex=startindex+len(query.lower())
    # example quote[:startindex]+"<span id="highlighted">"+quote[startindex:endindex]+"</mark>"+quote[endindex:]
    return (quote[:startindex],quote[startindex:endindex],quote[endindex:])

# Grab all the quotes that contains user_input
def grab_all_quotes(user_iput):
    return quotes.query.filter(quotes.quote.contains(user_iput)).all()

# Seak Yith
# combine lists into a tuple
def merge(list1, list2, list3, list4):
    mergedList= tuple(zip(list1, list2, list3, list4))
    return mergedList

# Seak Yith
# Shane Hazelquist (query for highlighting and logging statement)
# store all the quotes into a tuple for display
def store_all_quotes(quotes, query):
    season = []
    episode = []
    character = []
    actualQuote = []

    for x in quotes:
        season.append(x.episode.season)
        episode.append(x.episode.episode)
        character.append(x.character.name)
        actualQuote.append(highlight(query,x.quote))
        x.logging[0].inc()# increment log

    db.session.commit()# save logging information to model session

    result_quotes = merge(season, episode, character, actualQuote)

    return result_quotes

def page_number(number, per_page):
    if number % per_page == 0:
        page_number = int(number/per_page)
    else:
        page_number = int(number/per_page) + 1
    return page_number
