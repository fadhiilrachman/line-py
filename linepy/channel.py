# -*- coding: utf-8 -*-
from .client import LineClient
from .timeline import LineTimeline
from types import *

class LineChannel(LineTimeline):
    isLogin       = False
    channelId     = None
    profileDetail = None

    client      = None
    server      = None
    
    channelAccessToken      = None
    channelToken            = None
    obsToken                = None
    channelRefreshToken     = None
    channelTokenExpiration  = None

    def __init__(self, client, channelId=None):
        if type(client) is not LineClient:
            raise Exception("You need to set LineClient instance to initialize LineChannel")
        self.client = client
        self.server = client.server
        self.channelId = channelId
        self.login()

    def login(self):
        if self.channelId is None:
            self.channelId=self.server.CHANNEL_ID['LINE_TIMELINE']
        result = self.approveChannelAndIssueChannelToken(self.channelId)
        
        self.channelAccessToken     = result.channelAccessToken
        self.channelToken           = result.token
        self.obsToken               = result.obsToken
        self.channelRefreshToken    = result.refreshToken
        self.channelTokenExpiration = result.expiration
        self.isLogin = True

        self.createSession()

    def createSession(self):
        if self.isLogin:
            self.server.setChannelHeadersWithDict({
                'Content-Type': 'application/json',
                'User-Agent': self.server.USER_AGENT,
                'X-Line-Mid': self.client.profile.mid,
                'X-Line-Carrier': self.server.CARRIER,
                'X-Line-Application': self.server.APP_NAME,
                'X-Line-ChannelToken': self.channelAccessToken
            })
            channelInfo = self.getChannelInfo(self.channelId)
            if self.channelId == self.server.CHANNEL_ID['LINE_TIMELINE']:
                LineTimeline.__init__(self)
                self.profileDetail = self.getProfileDetail()
                self.client.setChannelToModels(self)
            self.client.log('[%s] : Success login to %s' % (self.client.profile.displayName, channelInfo.name))

    def approveChannelAndIssueChannelToken(self, channelId):
        return self.client.channel.approveChannelAndIssueChannelToken(channelId)

    def issueChannelToken(self, channelId):
        return self.client.channel.issueChannelToken(channelId)

    def getChannelInfo(self, channelId, locale='EN'):
        return self.client.channel.getChannelInfo(channelId, locale)

    def revokeChannel(self, channelId):
        return self.client.channel.revokeChannel(channelId)