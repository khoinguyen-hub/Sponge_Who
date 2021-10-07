# Khoi Nguyen
# 9/9/2021
# work on retrieving user's input
# parse and clean up text files 
# populating databases
# return the speaker of the quote using user's input and query

#imports
from model import *
import os

# Function to parse text file into a dictionary
#  -key is line number
#  -value is a list of 2 values
#  -value[0] is speaker
#  -value[1] is quote
#  -still have junks in text files
#  -not yet finished, only parse one file
def parseTextFile():
    key = 0
    transcript_dict = {}
    # change local path depends on your file path
    folder = r'SpongeBob_SquarePants_Transcripts'
    for path, dirc, files in os.walk(folder):
        for filename in files:
            print(filename)
            with open(path + os.sep + filename, encoding="utf8") as file:
                for line in file:
                    count = 0
                    line.strip()
                    for string in line:
                        if string == ":":
                            value = line.split(":", 1)
                            value.append(filename)
                            transcript_dict[key] = value
                            key += 1
                            break
                        elif string == "[" and count == 0:
                            key += 1
                            break
                        elif string == "\n":
                            continue
                        else:
                            count += 1
    return transcript_dict

# Function to clean up junks from parsed files and return cleaned dictionary
#  -remove any unwanted characters and strings
#  -unfinished, still missing junk options
def cleanDict(dict):
    newdict = {}
    for key, items in dict.items():
        for x in items[1]:
            if x == "\n":
                string = items[1].strip("\n")
                items[1] = string
            elif x == "/":
                string = items[1].strip("/")
                items[1] = string
        newdict[key] = items
        for x in items[0]:
            if x == '(':
                string = items[0].split(' ') 
                items[0] = string[0]
                newdict[key] = items
        else:
            newdict[key] = items
    return newdict

# Function to populate characters table
def populateDatabaseCharacters(dict):
    print('start to populate character data')
    for key, items in dict.items():
        character = characters(items[0])
        missing = characters.query.filter_by(name=items[0]).first()
        if missing is None:
            db.session.add(character)
            print('populating character '+str(key))
    db.session.commit()
    print('populated characters')

# Function to populate Quotes table
def populateDatabaseQuotes(dict):
    print('start to populate quote data')
    for key, items in dict.items():
        string = items[1]
        character = characters.query.filter_by(name=items[0]).first()
        episode = episodes.query.filter_by(ep_filename=items[2]).first()
        quote = quotes(episode.id, key, character.id, string)
        db.session.add(quote)
        print('populating quote '+str(key))
    db.session.commit()
    print('populated quotes')

# For testing
# def main():
    # Uncomment this and run it on first set up for testing.
    # db.create_all()
    # dict = parseTextFile()
    # newdict = cleanDict(dict)
    # populateDatabaseCharacters(newdict)
    # populateDatabaseQuotes(newdict)

    # print("Please enter a quote from spongebob:\n")
    # user_input = input()
    # result = quotes.query.filter(quotes.quote.contains(user_input)).all()
    # for x in result:
    #     print("Season: " + str(x.episode.season) + " ep: " + str(x.episode.episode) + " title: " + x.episode.ep_name + str(x.character.name) + ": " + x.quote)

# if __name__=='__main__':
#     main()