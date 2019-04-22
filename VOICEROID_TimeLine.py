#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json
from os import path as ospath
import re
import subprocess
import tweepy

# Check Config.json
fpath = '{0}\\Config.json'.format(ospath.dirname(ospath.abspath(__file__)))
if ospath.exists(fpath):
    fp = codecs.open(fpath, 'r', 'utf-8')
    conf = json.load(fp)
    fp.close()
else:
    # Initial setting
    PATH_VRX = input('Drag and Drop vrx.exe : ')
    PATH_VOICEROID = input('Drag and Drop VOICEROID.exe : ')
    CK = input("Input Consumer Key (API Key) : ")
    CS = input("Input Consumer Secret (API Secret) : ")
    AT = input("Input Access Token : ")
    AS = input("Input Access Token Secret : ")
    conf = {'path': {'vrx': PATH_VRX, 'voiceroid': PATH_VOICEROID},
            'api': {'ck': CK, 'cs': CS, 'at': AT, 'as': AS}}
    # Save to Config.json
    fp = codecs.open(fpath, 'w', 'utf-8')
    json.dump(conf, fp, indent=4)
    fp.close()

# Call voiceroid.exe and vrx.exe
pvr = subprocess.Popen(conf['path']['voiceroid'])
pvrx = subprocess.Popen(conf['path']['vrx'])

# Set Tweepy api
auth = tweepy.OAuthHandler(conf['api']['ck'], conf['api']['cs'])
auth.set_access_token(conf['api']['at'], conf['api']['as'])
api = tweepy.API(auth)


# Override Listener
class Listener(tweepy.StreamListener):

    def on_status(self, status):
        # NG word
        try:
            for word in conf['NG']['word']:
                if status.text.find(word) != -1:
                    return True
        except KeyError:
            pass
        # NG client
        try:
            if status.source in conf['NG']['client']:
                return True
        except KeyError:
            pass
        # NG user_id
        try:
            if status.user.id in conf['NG']['user_id']:
                return True
        except KeyError:
            pass
        # NG user_screen_name
        try:
            if status.user.screen_name in conf['NG']['user_screen_name']:
                return True
        except KeyError:
            pass
        # Only list User
        try:
            if status.user.screen_name not in conf['list']['user']:
                return True
        except KeyError:
            pass
        # replace Tweet text
        try:
            for retxt in conf['re']:
                status.text = re.sub(retxt, conf['re'][retxt], status.text)
        except KeyError:
            pass
        # escapeされてるので大丈夫っぽい(?)
        cmd = "{0} {1}さんのつぶやき。{2}".format(
            conf['path']['vrx'], status.user.name, status.text)
        subprocess.call(cmd)
        return True

listener = Listener()
stream = tweepy.Stream(auth, listener)
try:
    stream.userstream()
except:
    pvr.kill()
    pvrx.kill()
