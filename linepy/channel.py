# -*- coding: utf-8 -*-
from .client import LineClient
from types import *
import urllib
import requests
import json

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
    def getAlbum(self, gid):
        url = "http://gd2.line.naver.jp/mh/album/v3/albums?type=g&sourceType=TALKROOM&homeId=" + gid
        r = self.server.get_content(url, headers=self.server.channelHeaders)
        return r.json()
    
    @loggedIn
    def deleteAlbum(self,gid,albumId):
        r = requests.delete(
            "http://gd2.line.naver.jp/mh/album/v3/album/" + albumId + "?homeId=" + gid,
            headers = self.server.channelHeaders,
            )
        return r.json()
    
    @loggedIn
    def postNote(self, gid, text):
        payload = {"postInfo":{"readPermission":{"homeId":gid}},
                   "sourceType":"GROUPHOME",
                   "contents":{"text":text}
                   }
        r = requests.post(
            "http://gd2.line.naver.jp/mh/api/v27/post/create.json",
            headers = self.server.channelHeaders,
            data = json.dumps(payload)
            )
        return r.json()
    
    def save_image(self,filename, image):
        with open(filename, "wb") as fout:
            fout.write(image)
     
    @loggedIn
    def getAlbumImage(self,albumId,oid,gid):
        url = self.server.LINE_OBS_DOMAIN + "/album/a/download.nhn?ver=1.0&oid="+oid
        h = {
            "User-Agent" : self.server.UserAgent,
            "X-Line-ChannelToken" : self.channelAccessToken,
            "X-Line-Application": self.server.AppName,
            "X-Line-Album" : albumId,
            "X-Line-Mid" : gid,
            "Accept-Encoding" : "gzip",
            "Connection" : "Keep-Alive",
        }
        r = requests.get(url,headers = h)
        #print(r.content)
        print(r.text)
        print(r.status_code)
        self.save_image(str(oid)+".jpg",r.content)
    
    @loggedIn
    def getNote(self,gid, commentLimit, likeLimit):
        url = "http://gd2.line.naver.jp/mh/api/v27/post/list.json?homeId=" + gid + "&commentLimit=" + commentLimit + "&sourceType=TALKROOM&likeLimit=" + likeLimit
        r = self.server.get_content(url, headers=self.server.channelHeaders)
        return r.json()
        
    @loggedIn
    def addtoAlbum(self,gid,albumId,path,oid):
        h = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent" : "Line/7.5.2 iPad4,1 9.0.2",
            "X-Line-Mid" : self.mid,
            "X-Line-Album" : albumId,
            "x-lct" : self.channelAccessToken
        }
        files = {
            'file': open(path, 'rb'),
        }
        p = {
            "userid" : self.mid,
            "type" : "image",
            "oid" : oid,
            "ver" : "1.0"
        }
        data = {
            'params': json.dumps(p)
        }
        r = self.server.post_content(url="http://obs-jp.line-apps.com:443/oa/album/a/object_info.nhn",headers=h,data=data,files=files)
        print("CAME")
        return r.json()
    
    @loggedIn
    def getCover(self, mid):
        if mid is None:
            mid=self.mid
        home = self.getHome(mid)
        objId = home["result"]["homeInfo"]["objectId"]
        return self.server.LINE_OBS_DOMAIN + "/myhome/c/download.nhn?userid=" + mid + "&oid=" + objId