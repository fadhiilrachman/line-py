# -*- coding: utf-8 -*-
from akad.ttypes import Message
from .auth import LineAuth
from .models import LineModels
from .talk import LineTalk
from .square import LineSquare
from .call import LineCall
from random import randint

import json

class LineClient(LineAuth, LineModels, LineTalk, LineSquare, LineCall):

    customThrift = None

    def __init__(self, id=None, passwd=None, authToken=None, certificate=None, systemName=None, appName=None, showQr=False, keepLoggedIn=True, customThrift=None):
        
        LineAuth.__init__(self)
        if customThrift:
            self.customThrift = customThrift
        if not (authToken or id and passwd):
            self.qrLogin(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr)
        if authToken:
            self.tokenLogin(authToken=authToken, appName=appName)
        if id and passwd:
            self.login(_id=id, passwd=passwd, certificate=certificate, systemName=systemName, appName=appName, keepLoggedIn=keepLoggedIn)

        self.profile    = self.talk.getProfile()
        self.groups     = self.talk.getGroupIdsJoined()

        LineModels.__init__(self)
        LineTalk.__init__(self)
        LineSquare.__init__(self)
        LineCall.__init__(self)