# -*- coding: utf-8 -*-
from datetime import datetime
from .channel import Channel

import json, time, base64

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin
    
class Timeline(Channel):

    def __init__(self):
        Channel.__init__(self, self.channel, self.server.CHANNEL_ID['LINE_TIMELINE'], False)
        self.tl = self.getChannelResult()
        self.__loginTimeline()
        
    def __loginTimeline(self):
        self.server.setTimelineHeadersWithDict({
            'Content-Type': 'application/json',
            'User-Agent': self.server.USER_AGENT,
            'X-Line-Mid': self.profile.mid,
            'X-Line-Carrier': self.server.CARRIER,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-ChannelToken': self.tl.channelAccessToken
        })
        self.profileDetail = self.getProfileDetail()

    """Timeline"""

    @loggedIn
    def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
        params = {'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'order': order}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/feed/list.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1, likeLimit=1):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'LINE_PROFILE_COVER'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/post/list.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def getProfileDetail(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        params = {'userMid': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v1/userpopup/getDetail.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def updateProfileCoverById(self, objId):
        params = {'coverImageId': objId}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/home/updateCover.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def getProfileCoverId(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        home = self.getProfileDetail(mid)
        return home['result']['objectId']

    @loggedIn
    def getProfileCoverURL(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        home = self.getProfileDetail(mid)
        params = {'userid': mid, 'oid': home['result']['objectId']}
        return self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/myhome/c/download.nhn', params)

    """Post"""

    @loggedIn
    def createPost(self, text, holdingTime=None):
        params = {'homeId': self.profile.mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/post/create.json', params)
        payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime
        data = json.dumps(payload)
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def sendPostToTalk(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {'receiveMid': mid, 'postId': postId}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/post/sendPostToTalk.json', params)
        r = self.server.getContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def createComment(self, mid, postId, text):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/comment/create.json', params)
        data = {'commentText': text, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def deleteComment(self, mid, postId, commentId):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/comment/delete.json', params)
        data = {'commentId': commentId, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def likePost(self, mid, postId, likeType=1001):
        if mid is None:
            mid = self.profile.mid
        if likeType not in [1001,1002,1003,1004,1005,1006]:
            raise Exception('Invalid parameter likeType')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/like/create.json', params)
        data = {'likeType': likeType, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/like/cancel.json', params)
        data = {'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        return r.json()

    """Group Post"""

    @loggedIn
    def createGroupPost(self, mid, text):
        payload = {'postInfo': {'readPermission': {'homeId': mid}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        data = json.dumps(payload)
        r = self.server.postContent(self.server.LINE_TIMELINE_API + '/v39/post/create.json', data=data, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def createGroupAlbum(self, mid, name):
        data = json.dumps({'title': name, 'type': 'image'})
        params = {'homeId': mid,'count': '1','auto': '0'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album.json', params)
        r = self.server.postContent(url, data=data, headers=self.server.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Create a new album failure.')
        return True

    @loggedIn
    def deleteGroupAlbum(self, mid, albumId):
        params = {'homeId': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.server.deleteContent(url, headers=self.server.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Delete album failure.')
        return True
    
    @loggedIn
    def getGroupPost(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
        params = {'homeId': mid, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'TALKROOM'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/post/list.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    """Group Album"""

    @loggedIn
    def getGroupAlbum(self, mid):
        params = {'homeId': mid, 'type': 'g', 'sourceType': 'TALKROOM'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/albums.json', params)
        r = self.server.getContent(url, headers=self.server.timelineHeaders)
        return r.json()

    @loggedIn
    def changeGroupAlbumName(self, mid, albumId, name):
        data = json.dumps({'title': name})
        params = {'homeId': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.server.putContent(url, data=data, headers=self.server.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Change album name failure.')
        return True

    @loggedIn
    def addImageToAlbum(self, mid, albumId, path):
        file = open(path, 'rb').read()
        params = {
            'oid': int(time.time()),
            'quality': '90',
            'range': len(file),
            'type': 'image'
        }
        hr = self.server.additionalHeaders(self.server.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId,
            'x-obs-params': self.genOBSParams(params,'b64')
        })
        r = self.server.getContent(self.server.LINE_OBS_DOMAIN + '/album/a/upload.nhn', data=file, headers=hr)
        if r.status_code != 201:
            raise Exception('Add image to album failure.')
        return r.json()

    @loggedIn
    def getImageGroupAlbum(self, mid, albumId, objId, returnAs='path', saveAs=''):
        if saveAs == '':
            saveAs = self.genTempFile('path')
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        hr = self.server.additionalHeaders(self.server.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId
        })
        params = {'ver': '1.0', 'oid': objId}
        url = self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/album/a/download.nhn', params)
        r = self.server.getContent(url, headers=hr)
        if r.status_code == 200:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download image album failure.')
