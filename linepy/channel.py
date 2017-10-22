# -*- coding: utf-8 -*-
from .client import LineClient
from types import *

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin
    
class LineChannel(object):
    isLogin     = False
    channelId   = None

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
            self.channelId='1341209950'     # Timeline Channel Id
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
            self.server.setChannelHeaders('Content-Type', 'application/json')
            self.server.setChannelHeaders('User-Agent', self.server.USER_AGENT)
            self.server.setChannelHeaders('X-Line-Mid', self.client.profile.mid)
            self.server.setChannelHeaders('X-LCT', self.channelAccessToken)
            
            channelInfo = self.getChannelInfo(self.channelId)
            self.client.log('[%s] Success login to %s' % (self.client.profile.displayName, channelInfo.name))

    def approveChannelAndIssueChannelToken(self, channelId):
        return self.client.channel.approveChannelAndIssueChannelToken(channelId)

    def issueChannelToken(self, channelId):
        return self.client.channel.issueChannelToken(channelId)

    def getChannelInfo(self, channelId, locale='EN'):
        return self.client.channel.getChannelInfo(channelId, locale)

    def revokeChannel(self, channelId):
        return self.client.channel.revokeChannel(channelId)
        
    """TIMELINE"""

    @loggedIn
    def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
        params = {'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'order': order}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/feed/list', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def getHomeProfile(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
        if mid is None:
            mid = self.client.profile.mid
        params = {'homeId': mid, 'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'LINE_PROFILE_COVER'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/post/list', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def getProfileDetail(self, mid):
        if mid is None:
            mid = self.client.profile.mid
        params = {'userMid': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v1/userpopup/getDetail', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    """COMMENT POST"""

    @loggedIn
    def createComment(self, mid, postId, text):
        if mid is None:
            mid = self.client.profile.mid
        if postId is None:
            raise Exception('Please provide postId')
        if text is None:
            raise Exception('Please provide text')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v23/comment/create', params)
        data = {
            'commentText': text,
            'activityExternalId': postId,
            'actorId': mid
        }
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def deleteComment(self, mid, postId, commentId):
        if mid is None:
            mid = self.client.profile.mid
        if postId is None:
            raise Exception('Please provide postId')
        if commentId is None:
            raise Exception('Please provide commentId')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v23/comment/delete', params)
        data = {
            'commentId': commentId,
            'activityExternalId': postId,
            'actorId': mid
        }
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    """LIKE POST"""

    @loggedIn
    def likePost(self, mid, postId, likeType=1001):
        if mid is None:
            mid = self.client.profile.mid
        if postId is None:
            raise Exception('Please provide postId')
        if likeType not in [1001,1002,1003,1004,1005,1006]:
            raise Exception('Invalid parameter likeType')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v23/like/create', params)
        data = {
            'likeType': likeType,
            'activityExternalId': postId,
            'actorId': mid
        }
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.client.profile.mid
        if postId is None:
            raise Exception('Please provide postId')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v23/like/cancel', params)
        data = {
            'activityExternalId': postId,
            'actorId': mid
        }
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()
    
    """Contact"""

    @loggedIn
    def getProfileCoverURL(self, mid):
        if mid is None:
            mid = self.client.profile.mid
        home = self.getProfileDetail(mid)
        params = {'userid': mid, 'oid': home["result"]["objectId"]}
        return self.server.urlEncode(self.server.LINE_OBS_DOMAIN, "/myhome/c/download.nhn", params)