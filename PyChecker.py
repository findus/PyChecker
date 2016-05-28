# -*- coding: utf-8 -*-
import requests
import json
import notify2
import time
from os.path import expanduser
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

firststart = True
dictionary = dict()


def printsummary(json):
    notify2.init('Streams Online')
    message = ''
    for channel in json['streams']:
        message += " {0:20}     {1:6}\n    {2}\n\n".format(channel['channel']['display_name'],str(channel['viewers']),channel['game'])
    message = message[:-2]
    showmessage(message)

def showmessage(message):
    n = notify2.Notification("Streams:",message,"notification-message-im")
    n.show()

def loadFromFile():
    streamfile = open(expanduser("~")+"/.config/.pychecker/streams")
    channels = streamfile.read().replace("\n","").split(",")
    return channels

def downloadjson(channellist):
    link = 'https://api.twitch.tv/kraken/streams/?channel=%s' % ','.join(channels)
    #print "Connect to %s" % link
    s = requests.get(link)
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
            #print channel
            for listchannel in parsedJson['streams']:                #print channel,'=',listchannel['channel']['name']
                if listchannel['channel']['name'] == channel:
                    #print "Channel Found %s , State in dict: %s" % (channel,dictionary[channel])
                    found = True
                    if dictionary[channel] == False:
                        onlineoffline +=  "  %s \n" % listchannel['channel']['display_name']
                        dictionary[channel] = True
            #print "ended iteration, %s, %s, %s" % (found,dictionary[channel],channel)
            if found == False and dictionary[channel] == True:
                onlineoffline +=  "  %s \n" % listchannel['channel']['display_name']
                dictionary[channel] = False
        if(len(onlineoffline) > 0):
            showmessage(onlineoffline)
        time.sleep(60)


channels = loadFromFile()

for channelname in channels:
    dictionary[channelname] = False
