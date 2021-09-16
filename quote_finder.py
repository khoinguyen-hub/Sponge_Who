#!/usr/bin/env python3
"""
# Authors:
# -shazelquist
# 
# Super lite Prototype of quote_finder database operations
# Directive:
# -Perform psuedo db operations
# -Perform as a standalone application for debugging info
"""
# 
# Authors:
# -shazelquist
# 

# Imports:
from sys import argv
# Directive:
# -Establish a very rudamentry form of the project
# -Can run as standalone

Fake_Database=[] #fake database, list of dicts

def populate_fake_database(path="Tea_at_the_Treedome.txt",Season=1,Episode=3):# currently set for default
    """Parse file lines into fake database"""
    # should be called multiple times to add each episode
    global Fake_Database # make global dictionary writable
    with open(path) as inputfile:# open file
        lines=inputfile.read().split('\n')# read text in file, and split('\n')
        speaker="NULL"
        quote="NULL"
        i=0# increment for episode linecount

        for line in lines:
            if line!="":
                if ":" in line:#check for speaker indication
                    speaker=line[:line.index(':')]
                    quote=line[line.index(':')+1:]
                    #print('Speaker:"{}" Quote:"{}"'.format(speaker,quote))
                else:# no speaker, assume previous speaker
                    quote=line
                    #print('Speaker:"{}" Quote:"{}"'.format(speaker,quote))
                Fake_Database.append({'Speaker':speaker,'Quote':quote,'LineNumber':i,
                'Season':Season,'Episode':Episode})
                i+=1

def searchstring(query:str):
    """Find query in very basic form assuming query is a substring"""
    # Guess matching
    # Select * from Quote_table where CONTAINS(Quote,query);
    results=[]# Accumulator for possitive hits

    for entry in Fake_Database:# for each entry in db list
        if query in entry['Quote']:#if query is a substring of given quote
            results.append(entry)# add to results
    return results

def main():
    """Main function for debugging"""
    print('Hello, welcome to the quote_finder main')
    print('Initial fake database:{}'.format(Fake_Database))
    populate_fake_database()#populated fake database with ripped txt file
    print('Database populated:{} Quote entries'.format(len(Fake_Database)))

    res=None
    if len(argv)>1:# use argument 1 if given
        res=searchstring(argv[1])
    else:# no argument given, request input
        res=searchstring(input("Please query a quote from episode 1c:'Episode_Transcript:_Tea_at_the_Treedome' "))
    if res:# Results obtained
        print('{} Results:\n{}'.format(len(res),res))
    else:# No hits, inform user
        print('No results for query, please try again')

if __name__=='__main__':
    main()
