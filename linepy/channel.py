# -*- coding: utf-8 -*-
from .client import LineClient
from types import *

import urllib

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin
    
class LineChannel(object):
    _channel = None
    isLogin = False
    
    client=None
    mid=None
    authToken=None
    
    channelAccessToken = None

    def __init__(self, client, channel_id=None):
        if type(client) is not LineClient:
            raise Exception("You need to set LineClient instance to initialize LineChannel")
        self.client = client
        self.server = client.server
        self.mid=self.client.profile.mid
        self.authToken=self.client.authToken
        self._channel = self.client.channel
        if channel_id is None:
            channel_id='1341209950'
        self.login(channel_id=channel_id)

    def login(self, channel_id=None):
        result = self._channel.issueChannelToken(channel_id)
        
        self.isLogin = True
        self.channelAccessToken = result.channelAccessToken
        
        self.server.set_channelHeaders('X-Line-Mid', self.mid)
        self.server.set_channelHeaders('X-LCT', self.channelAccessToken)
        
    """MYHOME"""

    @loggedIn
    def getHome(self, mid):
        if mid is None:
            mid=self.mid
        params = {'homeId': mid, 'commentLimit': '1', 'sourceType': 'LINE_PROFILE_COVER', 'likeLimit': '1'}
        url = self.server.LINE_HOST_DOMAIN + '/mh/api/v27/post/list.json?' + urllib.parse.urlencode(params)
        r = self.server.get_content(url, headers=self.server.channelHeaders)
        return r.json()
    
    @loggedIn
    def getCover(self, mid):
        if mid is None:
            mid=self.mid
        home = self.getHome(mid)
        objId = home["result"]["homeInfo"]["objectId"]
        return self.server.LINE_OBS_DOMAIN + "/myhome/c/download.nhn?userid=" + mid + "&oid=" + objId