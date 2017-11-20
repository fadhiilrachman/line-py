# -*- coding: utf-8 -*-
from akad.ttypes import Message
from datetime import datetime
import time, base64
import json, shutil

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin
    
class LineModels(object):
        
    """Text"""
    
    def log(self, text):
        print("[%s] %s" % (str(datetime.now()), text))
        
        
    # It's still development, if you have a working code please pull it on linepy GitHub Repo
    @loggedIn
    def updateProfileCover(self, path):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel is required for acquire this action.')
        else:
            headers, optionsHeaders={}, {}
            optionsHeaders.update(self.server.channelHeaders)
            optionsHeaders.update({
                'access-control-request-headers': 'content-type,x-obs-params,x-obs-userdata,X-Line-ChannelToken',
                'access-control-request-method': 'POST'
            })
            opt_r = self.server.optionsContent(self.server.LINE_OBS_DOMAIN + '/myhome/c/upload.nhn', headers=optionsHeaders)
            if opt_r.status_code == 200:
                headers.update(self.server.channelHeaders)
                self.server.setChannelHeaders('Content-Type', 'image/jpeg')
                file=open(path, 'rb')
                files = {
                    'file': file
                }
                params = {
                    'name': 'media',
                    'type': 'image',
                    'userid': self.profile.mid,
                    'ver': '1.0',
                }
                data={
                    'params': json.dumps(params)
                }
                r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/myhome/c/upload.nhn', data=data, files=files)
                if r.status_code != 201:
                    raise Exception('Update profile cover failure.')
                return True
            else:
                raise Exception('Cannot set options headers.')
    
    
    @loggedIn
    def updateGroupCover(self, gid, path):
        params = '{"ver": "1.0", "type": "image", "name": "%s", "oid": "%s"}' % (int(time.time() * 1000), gid)
        with open(path, "rb") as f:
            body = base64.b64encode(f.read())
        req_bytes = base64.b64decode(body)
        Head={
            "Connection":"keep-alive",
            "Origin":"null",
            "X-LAL":"ja",
            "X-Line-Access":self.authToken,
            "User-Agent": self.server.UserAgent,
            "X-Line-Application": self.server.AppName,
            "Content-Type":"image/png",
            "Access-Control-Allow-Origin": "*",
            "x-obs-params": base64.b64encode(params.encode('utf-8')),
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ja,en-US;q=0.8,en;q=0.6",
            "Content-Length": str(len(req_bytes))
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + "/talk/g/upload.nhn", data=req_bytes, headers=Head)
        if r.status_code != 201:
            raise Exception('Update failure.')
            return False
        else:
            return True
            
    @loggedIn
    def sendGif(self, _to, path):
        with open(path, "rb") as f:
            body = base64.b64encode(f.read())
        req_bytes = base64.b64decode(body)
        params = '{"reqseq":"0","cat":"original","range":"bytes 0-%s\/%s","oid":"reqseq","tomid":"%s","name":"test.gif","quality":"80","ver":"1.0","type":"image"}' % (str(len(req_bytes)-1),str(len(req_bytes)),_to)
        Head={
            "Content-Type":"image/gif",
            "Connection":"Keep-Alive",
            "Accept": "*/*",
            "User-Agent": self.server.UserAgent,
            "X-Line-Access":self.authToken,
            "x-obs-params": base64.b64encode(params.encode('utf-8')),
            "X-Line-Carrier": self.server.CARRIER,
            "X-Line-Application": self.server.AppName,
            "Content-Length": str(len(req_bytes))
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + "/r/talk/m/reqseq", data=req_bytes, headers=Head)
        if r.status_code != 201:
            raise Exception('Update failure.')
            return False
        else:
            return True
            
    @loggedIn
    def sendGifWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGif(to, path)
            
    @loggedIn
    def addImageToAlbum(self, gid, aid, path):
        with open(path, "rb") as f:
            body = base64.b64encode(f.read())
        req_bytes = base64.b64decode(body)
        params = '{"quality":"90","ver":"1.0","type":"image","range":"bytes 0-%s\/%s","oid":"%s","name":"%s"}' % (str(len(req_bytes)-1),str(len(req_bytes)),gid, datetime.now().strftime('timeline_%Y%m%d_%H%M%S.jpg'))
        Head={
            "content-Type":"image/jpeg",
            "connection":"Keep-Alive",
            "accept": "*/*",
            "X-Line-ChannelToken": self.server.channelHeaders['X-LCT'],
            "X-Line-Album": str(aid),
            "User-Agent": self.server.UserAgent,
            "x-obs-params": base64.b64encode(params.encode('utf-8')),
            "X-Line-Carrier": self.server.CARRIER,
            "X-Line-Application": self.server.AppName,
            "X-Line-Mid": gid,
            "Content-Length": str(len(req_bytes))
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + "/album/a/upload.nhn", data=req_bytes, headers=Head)
        if r.status_code != 201:
            raise Exception('Update failure.')
            return False
        else:
            return True
                
    # It's still development, if you have a working code please pull it on linepy GitHub Repo
    @loggedIn
    def uploadPicture(self, path):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel is required for acquire this action.')
        else:
            headers, optionsHeaders={}, {}
            optionsHeaders.update(self.server.channelHeaders)
            optionsHeaders.update({
                'access-control-request-headers': 'content-type,x-obs-params,x-obs-userdata,X-Line-ChannelToken',
                'access-control-request-method': 'POST'
            })
            opt_r = self.server.optionsContent(self.server.LINE_OBS_DOMAIN + '/r/myhome/tmp/'+id, headers=optionsHeaders)
            if opt_r.status_code == 200:
                headers.update(self.server.channelHeaders)
                self.server.setChannelHeaders('Content-Type', 'image/jpeg')
                file=open(path, 'rb')
                files = {
                    'file': file
                }
                params = {
                    'name': 'media',
                    'type': 'image',
                    'userid': self.profile.mid,
                    'ver': '1.0',
                }
                data={
                    'params': json.dumps(params)
                }
                r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/myhome/c/upload.nhn', data=data, files=files)
                if r.status_code != 201:
                    raise Exception('Update profile cover failure.')
                return True
            else:
                raise Exception('Cannot set options headers.')

    """Object"""

    @loggedIn
    def downloadObjectMsgId(self, path, messageId,filename=None, extension='data'):
        if filename == None: filename = messageId
        path_n = '%s/%s.%s' % (path, filename, extension)
        url = self.server.LINE_OBS_DOMAIN + '/talk/m/download.nhn?oid=%s' % messageId
        r = self.server.get_content(url)
        if r.status_code == 200:
            with open(path_n, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            return True
        else:
            raise Exception('Download object failure.')
        
    @loggedIn
    def sendImage(self, to_, path):
        M = Message(to=to_, text=None, contentType = 1)
        M.contentMetadata = None
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': M_id,
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    @loggedIn
    def sendVideo(self, to_, path):
        M = Message(to=to_, text=None, contentType = 2)
        M.contentMetadata = {
            'VIDLEN' : '60000',
            'DURATION' : '60000'
        }
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
        files = {
            'file': open(path, 'rb')
        }
        params = {
            'name': 'media',
            'oid': M_id,
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    @loggedIn
    def sendVoice(self, to_, path):
        M = Message(to=to_, text=None, contentType = 3)
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'voice_message',
            'oid': M_id,
            'size': len(open(path, 'rb').read()),
            'type': 'audio',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload voice failure.')
        return True

    @loggedIn
    def sendFile(self, to_, path, file_name=''):
        if file_name == '':
            import ntpath
            file_name = ntpath.basename(path)
        M = Message(to=to_, text=None, contentType = 14)
        file_size = len(open(path, 'rb').read())
        M.contentMetadata = {
            'FILE_NAME' : str(file_name),
            'FILE_SIZE' : str(file_size)
        }
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': file_name,
            'oid': M_id,
            'size': file_size,
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload file failure.')
        return True