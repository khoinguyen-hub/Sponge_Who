# Created by Khoi Nguyen
# This file contains functions for use from flask view to reduce 
# cluster in the view

from os.path import exists as file_exists
from .quote_search import *

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

# Grab all the quotes that contains user_input
def grab_all_quotes(user_iput):
    return quotes.query.filter(quotes.quote.contains(user_iput)).all()

# Seak Yith
# combine lists into a tuple
def merge(list1, list2, list3, list4):
    mergedList= tuple(zip(list1, list2, list3, list4))
    return mergedList

# Seak Yith
# store all the quotes into a tuple for display
def store_all_quotes(quotes):
    season = []
    episode = []
    character = []
    actualQuote = []

    for x in quotes:
        season.append(x.episode.season)
        episode.append(x.episode.episode)
        character.append(x.character.name)
        actualQuote.append(x.quote)

    result_quotes = merge(season, episode, character, actualQuote)

    return result_quotes

def page_number(number, per_page):
    if number % per_page == 0:
        page_number = int(number/per_page)
    else:
        page_number = int(number/per_page) + 1
    return page_number