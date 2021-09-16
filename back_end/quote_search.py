# Khoi Nguyen
# 9/9/2021
# work on retrieving user's input and compare with database's entry
# to return the speaker of the quote
from model import *

def parseTextFile():
    key = 0
    transcript_dict = {}
    with open("C:\\Users\Admin\Downloads\CPSC362\Sponge_Who\\back_end\Tea_at_the_Treedome.txt") as infl:
        for line in infl:
            count = 0
            line.strip()
            for string in line:
                if string == ":":
                    transcript_dict[key] = line.split(":")
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

def cleanDict(dict):
    newdict = {}
    for key, items in dict.items():
        for x in items[1]:
            if x == "\n":
                string = items[1].strip("\n")
                items[1] = string
            elif x == "/":
                string = items[1].strip("\n")
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

def populateDatabaseCharacters(dict):
    for key, items in dict.items():
        character = characters(items[0])
        missing = characters.query.filter_by(name=items[0]).first()
        if missing is None:
            db.session.add(character)
            db.session.commit()

def populateDatabaseQuotes(dict):
    for key, items in dict.items():
        string = items[1]
        character = characters.query.filter_by(name=items[0]).first()
        quote = quotes(1, key, (int(character.id)), string)
        db.session.add(quote)
        db.session.commit()

# use user input to search
# def search(userinput, dict):
#     newdict = {}
#     for x, y in dict.items():
#         if userinput in y[1]:
#             newdict[x] = y
#     return newdict

def main():
    db.create_all()
    dict = parseTextFile()
    newdict = cleanDict(dict)
    populateDatabaseCharacters(newdict)
    populateDatabaseQuotes(newdict)
    print(characters.query.all())
    print(quotes.query.all())
    # print("Please enter a quote from spongebob:\n")
    # user_input = input()
    
if __name__=='__main__':
    main()


