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

def populateDatabase(dict):
    for key, items in dict.items():
        if items[1].endswith('\n'):
            string = items[1]
            character = characters(items[0])
            missing = characters.query.filter_by(name=items[0]).first()
            if missing is None:
                db.session.add(character)
                db.session.commit()
                missing = characters.query.filter_by(name=items[0]).first()
                quote = quotes(1, key, missing.id, string[:-1])
                db.session.add(quote)
                db.session.commit()
            else:
                missing = characters.query.filter_by(name=items[0]).first()
                quote = quotes(1, key, missing.id, string[:-1])
                db.session.add(quote)
                db.session.commit()
        else:
            character = characters(items[0])
            missing = characters.query.filter_by(name=items[0]).first()
            if missing is None:
                db.session.add(character)
                db.session.commit()
                missing = characters.query.filter_by(name=items[0]).first()
                quote = quotes(1, key, missing.id, string[:-1])
                db.session.add(quote)
                db.session.commit()
            else:
                missing = characters.query.filter_by(name=items[0]).first()
                quote = quotes(1, key, missing.id, string[:-1])
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
    populateDatabase(dict)
    print((characters.query.all()))
    # print("Please enter a quote from spongebob:\n")
    # user_input = input()
    
if __name__=='__main__':
    main()


