# -*- coding: utf-8 -*-

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Channel(object):
    isLogin = False
    channelId     = None
    channelResult = None

    def __init__(self, client, channelId, showSuccess=True):
        self.client = client
        self.channelId = channelId
        self.showSuccess = showSuccess
        self.__loginChannel()

    def __logChannel(self, text):
        self.client.log('[%s] : Success login to %s' % (self.client.profile.displayName, text))

    def __loginChannel(self):
        self.isLogin = True
        self.channelResult  = self.approveChannelAndIssueChannelToken(self.channelId)
        self.__createChannelSession()

    @loggedIn
    def getChannelResult(self):
        return self.channelResult

    def __createChannelSession(self):
        channelInfo = self.getChannelInfo(self.channelId)
        if self.showSuccess:
            self.__logChannel(channelInfo.name)

    @loggedIn
    def approveChannelAndIssueChannelToken(self, channelId):
        return self.client.approveChannelAndIssueChannelToken(channelId)

    @loggedIn
    def issueChannelToken(self, channelId):
        return self.client.issueChannelToken(channelId)

    @loggedIn
    def getChannelInfo(self, channelId, locale='EN'):
        return self.client.getChannelInfo(channelId, locale)

    @loggedIn
    def revokeChannel(self, channelId):
        return self.client.revokeChannel(channelId)
