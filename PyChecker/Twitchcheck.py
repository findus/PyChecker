# -*- coding: utf-8 -*-
import requests
import json
import time
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

def printsummary(json):
    message = ''
    for channel in json['streams']:
        message += " {0:20}     {1:6}\n    {2}\n\n".format(channel['channel']['display_name'],str(channel['viewers']),channel['game'])
    message = message[:-2]
    showmessage(message)

def showmessage(message):
    if os.name == 'posix':
        notify2.init('Streams Online')
        n = notify2.Notification("Streams:",message,"notification-message-im")
        n.show()

def loadFromFile():
    streamfile = open(expanduser("~")+"/.config/.pychecker/streams")
    channels = streamfile.read().replace("\n","").split(",")
    return channels

def getToken():
    link = "https://id.twitch.itv/oauth2/authorize?client_id=hb7zvth15ub915hs3qw0h5c6xab0a1&redirect_uri=http://localhost&response_type=token&scope=analytics:read:games"
    s = requests.get(link)
    return s.text

def getUserID():
    link = "https://api.twitch.tv/helix/users?login=Fozruk_"
    headers = {'Client-ID' : 'hb7zvth15ub915hs3qw0h5c6xab0a1'}
    s = requests.get(link,headers=headers)
    json2 = json.loads(s.text)
    return json2["data"][0]["id"]

#TODO pagination
def getFollowedStreams():
    link = 'https://api.twitch.tv/helix/users/follows?first=100&from_id=%s' % getUserID()
    headers = {'Client-ID' : 'hb7zvth15ub915hs3qw0h5c6xab0a1'}
    s = requests.get(link,headers=headers)
    return json.loads(s.text)

def downloadjson(channellist):
    link = 'https://api.twitch.tv/kraken/streams/?channel=%s' % ','.join(channels)
    headers = {'Client-ID' : 'og1crpd047s8mo4ocshg1yf93x5ak3n'}
    #print "Connect to %s" % link
    s = requests.get(link,headers=headers)
    return json.loads(s.text)

def showList():
    json = downloadjson(channels)
    printsummary(json)

def startMainLoop():
    while True:
        parsedJson = downloadjson(channels)
        global firststart
        if firststart == True:
            #print "First"
            printsummary(parsedJson)
            firststart = False

        onlineoffline = ''
        #print "Else"
        for channel in dictionary.keys():
            found = False
            dictionary[channel]['urlname'] = channel
            #print channel
            for listchannel in parsedJson['streams']:
                #print channel,'=',listchannel['channel']['name']
                if listchannel['channel']['name'] == channel:
                    #print "Channel Found %s , State in dict: %s" % (channel,dictionary[channel])
                    found = True
                    foundchannel = dictionary[channel]

                    topic = listchannel['channel']['status']
                    game = listchannel['channel']['game']
                    name = listchannel['channel']['display_name']
                    viewers = listchannel['viewers']

                    foundchannel['topic'] = topic
                    foundchannel['game'] = game
                    foundchannel['name'] = name
                    foundchannel['viewers'] = viewers

                    if foundchannel['online'] == False:
                        onlineoffline +=  "  %s \n" % listchannel['channel']['display_name']
                        dictionary[channel]['online'] = True
            #print "ended iteration, %s, %s, %s" % (found,dictionary[channel],channel)
            if found == False and dictionary[channel]['online'] == True:
                onlineoffline +=  "  %s \n" % listchannel['channel']['display_name']
                dictionary[channel] = False
                dictionary[channel]['topic'] = ''
                dictionary[channel]['game'] = ''
        if(len(onlineoffline) > 0):
            showmessage(onlineoffline)
        time.sleep(60)


channels = loadFromFile()

for channelname in channels:
    dictionary[channelname] = {'name' : channelname, 'online' : False , "viewers" : 0 , 'topic' : '' , 'game' : '', 'urlname' : ''}


userID = getUserID()
