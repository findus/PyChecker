# -*- coding: utf-8 -*-
import requests
import json
import time
import traceback
import os
from os.path import expanduser
if os.name == 'posix':
    import notify2
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

firststart = True

dictionary = dict()
gameDict = dict()
userDict = dict()

headers = {'Client-ID' : 'og1crpd047s8mo4ocshg1yf93x5ak3n'}

def printsummary(json):
    message = ''
    for channel in json:
        message += " {0:20}     {1:6}\n    {2}\n\n".format(getUserName(channel['user_id']),str(channel['viewer_count']),getGameName(channel['game_id']))
    message = message[:-2]
    showmessage(message)

def printError(e):
    showmessage(e)

def showmessage(message):
    if os.name == 'posix':
        notify2.init('Streams Online')
        n = notify2.Notification("Streams:",message,"notification-message-im")
        n.show()

#def loadFromFile():
#    streamfile = open(expanduser("~")+"/.config/.pychecker/streams")
#    channels = streamfile.read().replace("\n","").split(",")
#    return channels

def getToken():
    link = "https://id.twitch.itv/oauth2/authorize?client_id=hb7zvth15ub915hs3qw0h5c6xab0a1&redirect_uri=http://localhost&response_type=token&scope=analytics:read:games"
    s = requests.get(link)
    return s.text

def getUserID():
    link = "https://api.twitch.tv/helix/users?login=Fozruk_"
    s = requests.get(link,headers=headers)
    json2 = json.loads(s.text)
    return json2["data"][0]["id"]

#TODO pagination
def getFollowedStreams(userID):
    link = 'https://api.twitch.tv/helix/users/follows?first=100&from_id=%s' % userID
    s = requests.get(link,headers=headers)
    return json.loads(s.text)

def getStreamIDs(followedStreamsResponse):
    return '&user_id='.join(map(lambda x: x['to_id'], followedStreamsResponse['data']))

def getStreamUserIDs(streamsResponse):
    return '&id='.join(map(lambda x: x['user_id'], streamsResponse))

def getGameIDs(streamsResponse):
    return '&id='.join(map(lambda x: x['game_id'], streamsResponse))

def getStreams():
    link = "https://api.twitch.tv/helix/streams?first=100&user_id=%s" % getStreamIDs(getFollowedStreams(userID))
    s = requests.get(link,headers=headers)
    meem =  json.loads(s.text)
    print meem
    return meem

def downloadjson(channellist):
    link = 'https://api.twitch.tv/kraken/streams/?channel=%s' % ','.join(channels)
    #print "Connect to %s" %displayk
    s = requests.get(link,headers=headers)
    return json.loads(s.text)

def fillUserDict(userlist):
    global userDict
    userDict = dict(map(lambda x: (x['id'],x['display_name']),userlist))

def fillGameDict(gamelist):
    global gameDict
    gameDict = dict(map(lambda x: (x['id'],x['name']),gamelist))

def showList():
    json = getStreams()['data']
    print(json)
    printsummary(json)

def fetchGameNames(gameIDs):
    link = "https://api.twitch.tv/helix/games?id=%s" % gameIDs
    s = requests.get(link,headers=headers)
    meem =  json.loads(s.text)['data']
    print "gamenames: %s" % meem
    return meem

def fetchUserNames(listOfUserIds):
    link = "https://api.twitch.tv/helix/users?id=%s" % listOfUserIds
    s = requests.get(link,headers=headers)
    print "UserIDs: %s" % s.text
    return json.loads(s.text)['data']

def getGameName(id):
    print type(id)
    print "get game for id: %s" % id
    if id == u'0':
        print "meem"
        return "-"
    else:
        print "xd"
    if id not in gameDict:
        global gameDict
        gameDict[id] = fetchGameNames(id)[0]['name']
    return gameDict[id]

def getUserName(id):
    print "Userdict Username for ID %s" % id
    if id not in userDict:
        global userDict
        print "UserID %s not in dict, will fetch" % id
        userDict[id] = fetchUserNames(id)[0]['display_name']
    return userDict[id]

def startMainLoop():
    while True:
        print "Enter loop"
        try:
            parsedJson = getStreams()['data']
            global firststart
            if firststart == True:
                #print "First"
                fillGameDict(fetchGameNames(getGameIDs(parsedJson)))
                fillUserDict(fetchUserNames(getStreamUserIDs(parsedJson)))
                printsummary(parsedJson)
                firststart = False

            onlineoffline = ''
            #print "Else"
            for channel in dictionary.keys():
                found = False
                #dictionary[channel]['urlname'] = channel
                #print parsedJson
                for listchannel in parsedJson:
                    #print channel,'=',listchannel['user_id']
                    if listchannel['user_id'] == channel:
                        print "Channel Found %s , State in dict: %s" % (channel,dictionary[channel])
                        #https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
                        found = True
                        foundchannel = dictionary[channel]

                        topic = listchannel['title']
                        game = getGameName(listchannel['game_id'])
                        name = getUserName(listchannel['user_id'])
                        print "Name for channel: %s" % name
                        viewers = listchannel['viewer_count']

                        foundchannel['topic'] = topic
                        foundchannel['game'] = game
                        foundchannel['name'] = name
                        foundchannel['viewers'] = viewers

                        if foundchannel['online'] == False:
                            onlineoffline +=  "  %s \n" % foundchannel['name']
                            dictionary[channel]['online'] = True
                if found == False and dictionary[channel]['online'] == True:
                    print dictionary[channel]
                    onlineoffline +=  "  %s \n" % getUserName(channel) 
                    dictionary[channel]['online'] = False
                    dictionary[channel]['topic'] = ''
                    dictionary[channel]['game'] = ''
            if(len(onlineoffline) > 0):
                showmessage(onlineoffline)
            print "finish loop"
            time.sleep(60)
        except Exception as e:
            print("Exception:",e)
            traceback.print_exc()
            time.sleep(10)
            printError("Error")
            pass
    print "end method"

userID = getUserID()
channels = getFollowedStreams(userID)

for channelname in channels['data']:
    dictionary[channelname['to_id']] = {'name' : channelname['to_id'], 'online' : False , "viewers" : 0 , 'topic' : '' , 'game' : '', 'urlname' : ''}

#startMainLoop()
