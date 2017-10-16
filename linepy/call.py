# -*- coding: utf-8 -*-
from .client import LineClient
from akad.ttypes import MediaType
from types import *

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You want to call the function, you must login to LINE")
    return checkLogin
    
class LineCall(object):
    isLogin = False
    
    _call = None
    client=None

    def __init__(self, client):
        if type(client) is not LineClient:
            raise Exception("You need to set LineClient instance to initialize LineCall")
        self.client = client
        self._call = self.client.call
        
    def acquireCallRoute(self, to):
        return self._call.acquireCallRoute(to)
        
    def acquireGroupCallRoute(self, groupId, mediaType=MediaType.AUDIO):
        return self._call.acquireGroupCallRoute(groupId, mediaType)

    def getGroupCall(self, ChatMid):
        return self._call.getGroupCall(ChatMid)
        
    def inviteIntoGroupCall(self, chatId, contactIds=[], mediaType=MediaType.AUDIO):
        return self._call.inviteIntoGroupCall(chatId, contactIds, mediaType)