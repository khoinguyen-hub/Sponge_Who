#!usr/bin/python3
"""
# Authors: shazelquist
#
# Directive: Grab information regarding episode & season data, parse into a format to populate
#
"""
# Authors
# -shazelquist

# Notes:
# -Full linting style and document not provided
# -Checks for 'WIKIPATH' environment variable, set in advance

# Imports:
import re # regular expressions
import requests # request webpage if not present
from model import * # grab model
from os import listdir, environ # compare to files, enviornment variables
from os.path import isfile # check for existing file
from bs4 import BeautifulSoup as BS # Pase information out of htmlpage


# Manage parsing from soup into friendlier source
# -Parses from web soup and returns info as dictionary
# -nonstandard imports to keep non-calls from breaking
# -returns dictionary {filename:{'Name':,'Season':,'Episode':,'Minor':}}
def get_episode_info(filelist:list,logging=True):
    """parse soup into episode information into easy structure {filename:{'Name':,'Season':,'Episode':,'Minor':}}. Takes (['list of avaliable transcript files'], True/False/None logging argument)"""

    # set up information regarding filenames
    filelink={fl.lower():fl for fl in filelist}# list of filenames
    linkeys=list(filelink.keys())
    soup=get_season_data()# retrieve soup either from file or web

    episodes={}#Episode name:(season, episode number, minor)
    if logging:# wipe current parsed debug file
        with open('parsed.txt','w', encoding='utf-8') as parsefile:
            parsefile.write('')
    season=0# season counter
    eplog=''# logging variable
    mtc=0# logging variable
    missing_transcripts=''# logging variable

    for tag in soup.find_all('th',id=re.compile("ep[0-9]+[a-z]{0,1}")):#find all episodes
        ep=tag.find_next_sibling(style='text-align:center')
        if ep.text=='1a':# Increment counter instead of searching, this method is easier
            season+=1
        if not ep.text[-1].isalpha():# check for those without minor and assign default
            minor=1 #a
            episode=int(ep.text)
        else:
            episode=int(ep.text[:-1])# seperate major from minor
            minor=ord(ep.text[-1])-96 # retrieve minor and convert to int
        name=ep.find_next_sibling('td').text[1:-1]
        # replace Digits, Cap first, ascii-fiy
        # probably a better way to write this expression
        fname=re.sub(r'[0-9\s.,\-:;?!"\']','',name).replace("&",'amp')# delete and replace characters
        fname=fname[0].capitalize()+fname[1:]# capitalize

        # fix manually check & fix known errors, should replace this in the future
        fname,upd=man_fix_parsing_errors(fname,tag)

        if logging:# write parsed entries to file for debugging
            eplog+=tag.text+'\n' # save episode code
            with open('parsed.txt','a', encoding='utf-8') as parsefile:
                parsefile.write('{}\n'.format(fname))

        if fname.lower()+'.txt' in linkeys:# reverse query to avoid key error
            fname=filelink[fname.lower()+'.txt']
            episodes[fname]={'Name':name,'Season':season,'Episode':episode,'Minor':minor}
            episodes[fname].update(upd)# apply update for fixups
        elif logging:
            mtc+=1
            missing_transcripts+='#{} : {} -> {}\n'.format(tag.text,name,fname)

    if logging: # write episode codes to debug
        with open('eplog.txt','w') as epl:
            epl.write(eplog)

    # manually add a special episode, not fit for model, but file is present
    episodes['SpongeBobsBigBirthdayBlowout.txt']={'Name':"SpongeBob's Big Birthday Blowout",'Season':12,'Episode':9,'Minor':"S"}

    if logging and mtc:# If there are missing transcripts, write them down
        mtfile='missing_transcripts.txt'
        print('{} missing transcripts with current parsing, wrote to {}'.format(mtc,mtfile))
        with open(mtfile,'w',encoding='utf-8') as missingt:
            missingt.write(missing_transcripts)

    return episodes

def man_fix_parsing_errors(filename,tag):#
    """Update infomation for entries that does not conform to regular grid standard or name conversion. Takes(filename, soup tag)"""
    update={}#filename:{'Name':,'Season':,'Episode':,'Minor':
    if tag.text=='123124': # two part episode, one file
        update['Name']='Truth or Square'
        update['Episode']=23
        update['Minor']=1
        filename='TruthorSquare'
    elif tag.text=='126':# two titles
        filename='TheClashofTriton'
        update['name']='The Clash of Triton'
    elif tag.text=='266':# two titles
        filename='EscapefromGloveWorld'
        update['name']='Escape from Glove World'
    elif tag.text=='98':# two titles
        filename='WhatEverHappenedtoSpongeBob'
        update['name']="What Ever Happened to SpongeBob?"
    elif tag.text=='142a':#Non-standard filename
        filename='Trenchbilles'
    elif tag.text=='149a':# two titles
        filename='YouDontKnowSpongeBob'
    elif tag.text=='111':# two titles
        filename="SpongeBobSquarePantsvstheBigOne"
        update['name']="SpongeBob SquarePants vs the Big One"
    elif tag.text=='85b':# Non-standard filename:utf-8 -> ascii
        filename='KrabslaMode'
    elif tag.text=='174b':# Non-standard filename
        filename='ForHeretoGo'
    elif tag.text=='237':# two titles
        update['name']='SpaceBob MerryPants'
        filename='GoonsontheMoon'
        update['name']='Goons on the Moon'
    elif tag.text=='61a':# parse error
        filename='FearofaKrabbyPatty'
        update['name']='Fear of a Krabby Patty'
        update['Season']=4
        update['episode']=1
        update['minor']=1
    return filename, update



# Manage retrieval from html source
# -reads information from a wiki page and writes to file
# -reads file and returns soup for populating
# -nonstandard imports to keep non-calls from breaking
def get_season_data():
    """retrieve information from the wiki, copy html to file, and soupify it. Returns BS4 soup"""

    if not isfile('wikidata.html') or input('Force pull from web? y/n? ')=='y':
        
        # Perform user checkup
        print("NOTE:\n-You must agree not to abuse this module, this pulls external information.")
        print("-You will not make multiple pull requests\n-You will not place pulled information in any repo")
        if input('Please type "I agree" in order to continue: ').lower()!='I agree'.lower():
            print('Exiting, user did not agree to requirements')
            return

        if 'WIKIPATH' in environ:# ask for wiki url if not in enviornment variables
            url=environ['WIKIPATH']
        else:
            url=input("Please enter the wiki/list_of_episodes source url path:").strip()
        print('Requesting from "{}"'.format(url))
        page=requests.get(url)
        with open('wikidata.html','wb') as writefile:
            writefile.write(page.content)

    print('Attempting to load given copy')
    with open('wikidata.html','rb') as source:
        html=source.read()
        print('wrote to wikidata.html')

    souped=BS(html,'html.parser')
    return souped

def createobjects(files, ep_data):
    """Create sqlalchemy modeled episode objects from episode data, ([files],{episode data}), returns list of objects"""
    #__init__(self,season,episode,minor,name,filename):
    objects=[]
    for f in files:# only create for known files
        ed=ep_data[f]
        objects.append(episodes(ed['Season'],ed['Episode'],ed['Minor'],ed['Name'],f))
    return objects # use create_all method

def main():
    """Main function in grab_episode, provides some debug functionality"""
    ep=get_episode_info(listdir("SpongeBob_SquarePants_Transcripts"),False)
    with open('out.txt','w',encoding='utf-8') as out:
        for k in ep:
            out.write('{}\t->\t{}\n'.format(k,ep[k]))

    keys=list(ep.keys())
    keys.sort()

    files=listdir("SpongeBob_SquarePants_Transcripts")
    errors=0
    print("Checking for errors: files -> parsed")
    for t in files:
        if t not in keys:
            errors+=1
            print("ERROR ON {}".format(t))
    if input('Do you want to populate {} items (y/n)? '.format(len(ep)))=='y':
        res=createobjects(files,ep)
        db.session.add_all(res)
        db.session.commit()
        print('items pushed to database')

if __name__=='__main__':
    main()
