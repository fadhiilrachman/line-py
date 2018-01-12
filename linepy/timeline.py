# -*- coding: utf-8 -*-
from datetime import datetime
import json, time, base64

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You want to call the function, you must login to LINE")
    return checkLogin
    
class LineTimeline(object):

    def __init__(self):
        if self.isLogin == True and self.channelId == self.server.CHANNEL_ID['LINE_TIMELINE']:
            self.client.log('[%s] : LineTimeline attached' % self.client.profile.displayName)
        
    """Timeline"""

    @loggedIn
    def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
        params = {'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'order': order}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/feed/list.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1, likeLimit=1):
        if mid is None:
            mid = self.client.profile.mid
        params = {'homeId': mid, 'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'LINE_PROFILE_COVER'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/post/list.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def getProfileDetail(self, mid=None):
        if mid is None:
            mid = self.client.profile.mid
        params = {'userMid': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v1/userpopup/getDetail.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def updateProfileCoverById(self, objId):
        params = {'coverImageId': objId}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v39/home/updateCover.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    """Post"""

    @loggedIn
    def createPost(self, text):
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v33/post/create.json', params)
        payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        data = json.dumps(payload)
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def createComment(self, mid, postId, text):
        if mid is None:
            mid = self.client.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v33/comment/create.json', params)
        data = {'commentText': text, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def deleteComment(self, mid, postId, commentId):
        if mid is None:
            mid = self.client.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v33/comment/delete.json', params)
        data = {'commentId': commentId, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def likePost(self, mid, postId, likeType=1001):
        if mid is None:
            mid = self.client.profile.mid
        if likeType not in [1001,1002,1003,1004,1005,1006]:
            raise Exception('Invalid parameter likeType')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v33/like/create.json', params)
        data = {'likeType': likeType, 'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.client.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v33/like/cancel.json', params)
        data = {'activityExternalId': postId, 'actorId': mid}
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        return r.json()

    """Group Post"""

    @loggedIn
    def createGroupPost(self, mid, text):
        payload = {'postInfo': {'readPermission': {'homeId': mid}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        data = json.dumps(payload)
        r = self.server.postContent(self.server.LINE_TIMELINE_API + '/v27/post/create.json', data=data, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def createGroupAlbum(self, mid, name):
        data = json.dumps({'title': name, 'type': 'image'})
        params = {'homeId': mid,'count': '1','auto': '0'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album.json', params)
        r = self.server.postContent(url, data=data, headers=self.server.channelHeaders)
        if r.status_code != 201:
            raise Exception('Create a new album failure.')
        return True

    @loggedIn
    def deleteGroupAlbum(self, mid, albumId):
        params = {'homeId': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.server.deleteContent(url, headers=self.server.channelHeaders)
        if r.status_code != 201:
            raise Exception('Delete album failure.')
        return True
    
    @loggedIn
    def getGroupPost(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
        params = {'homeId': mid, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'TALKROOM'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/post/list.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    """Group Album"""

    @loggedIn
    def getGroupAlbum(self, mid):
        params = {'homeId': mid, 'type': 'g', 'sourceType': 'TALKROOM'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/albums.json', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

    @loggedIn
    def changeGroupAlbumName(self, mid, albumId, name):
        data = json.dumps({'title': name})
        params = {'homeId': mid}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.server.putContent(url, data=data, headers=self.server.channelHeaders)
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
        hr = self.server.additionalHeaders(self.server.channelHeaders, {
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
        hr = self.server.additionalHeaders(self.server.channelHeaders, {
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
    
    """Contact"""

    @loggedIn
    def getProfileCoverURL(self, mid=None):
        if mid is None:
            mid = self.client.profile.mid
        home = self.getProfileDetail(mid)
        params = {'userid': mid, 'oid': home['result']['objectId']}
        return self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/myhome/c/download.nhn', params)