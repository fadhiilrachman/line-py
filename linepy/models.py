# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint

import json, shutil, time

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin
    
class LineModels(object):

    _channel = None
        
    def __init__(self):
        if self.isLogin == True:
            self.log("[%s] : Login success" % self.profile.displayName)

    def setChannelToModels(self, channel):
        self._channel = channel

    def genTempFileName(self):
        try:
            import tempfile
            return '%s/linepy-%s-%i.bin' % (tempfile.gettempdir(), int(time.time()), randint(0, 9))
        except:
            raise Exception('tempfile is required')

    """Text"""

    def log(self, text):
        print("[%s] %s" % (str(datetime.now()), text))

    """Group"""

    @loggedIn
    def updateGroupPicture(self, groupId, path):
        file=open(path, 'rb')
        files = {
            'file': file
        }
        params = {
            'name': 'media',
            'type': 'image',
            'oid': groupId,
            'ver': '1.0'
        }
        data={
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/g/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update group picture failure.')
        return True

    """Personalize"""
    
    @loggedIn
    def cloneContactProfile(self, mid):
        contact = self.getContact(mid)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        profile.pictureStatus = contact.pictureStatus
        self.updateProfileAttribute(8, profile.pictureStatus)
        return self.updateProfile(profile)

    @loggedIn
    def updateProfilePicture(self, path):
        file=open(path, 'rb')
        files = {
            'file': file
        }
        params = {
            'name': 'media',
            'type': 'image',
            'oid': self.profile.mid,
            'ver': '1.0',
        }
        data={
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/p/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True
        
    @loggedIn
    def updateProfileVideoPicture(self, path):
        try:
            from ffmpy import FFmpeg
            file=open(path, 'rb')
            files = {
                'file': file
            }
            params = {
                'name': 'media',
                'type': 'video',
                'oid': self.profile.mid,
                'ver': '2.0',
                'cat': 'vp.mp4'
            }
            data={
                'params': json.dumps(params)
            }
            r_vp = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/vp/upload.nhn', data=data, files=files)
            if r_vp.status_code != 201:
                raise Exception('Change profile video profile failure.')
            path_p = self.genTempFileName()
            ff = FFmpeg(inputs={'%s' % path: None}, outputs={'%s' % path_p: ['-ss', '00:00:4', '-vframes', '1']})
            ff.run()
            file2=open(path_p, 'rb')
            files = {
                'file': file2
            }
            params = {
                'name': 'media',
                'type': 'image',
                'oid': self.profile.mid,
                'cat': 'vp.mp4',
                'ver': '2.0'
            }
            data={
                'params': json.dumps(params)
            }
            r_p = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/p/upload.nhn', data=data, files=files)
            if r_p.status_code != 201:
                raise Exception('Change profile video picture failure.')
            return True
        except:
            raise Exception('You should install ffmpeg from apt and ffmpy from pypi')

    # It's still development, if you have a working code please pull it on linepy GitHub Repo
    @loggedIn
    def updateProfileCover(self, path):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel instance is required for acquire this action.')
        else:
            home = self._channel.getProfileDetail(self.profile.mid)
            headers= {}
            headers.update(self.server.channelHeaders)
            headers.update({'Content-Type': 'image/jpeg'})
            file=open(path, 'rb')
            files = {
                'file': file
            }
            params = {
                'name': 'media',
                'type': 'image/jpeg',
                'oid': home["result"]["objectId"],
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

    """Object"""

    def downloadFileURL(self, fileUrl, returnAs='path', saveAs=''):
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        if saveAs == '':
            saveAs = self.genTempFileName()
        r = self.server.getContent(fileUrl)
        if r.status_code == 200:
            with open(saveAs, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download file failure.')

    @loggedIn
    def downloadObjectMsg(self, path, messageId, returnAs='path', saveAs=''):
        if saveAs == '':
            saveAs = self.genTempFileName()
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        params = {'oid': messageId}
        url = self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/talk/m/download.nhn', params)
        r = self.server.getContent(url)
        if r.status_code == 200:
            with open(saveAs, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download object failure.')

    @loggedIn
    def forwardObjectMsg(self, to, msgId, contentType='image'):
        if contentType not in ['image','video','audio']:
            raise Exception('Type not valid.')
        data = {
            'name': 'media',
            'oid': 'reqseq',
            'reqseq': self.revision,
            'type': contentType,
            'tomid': to,
            'copyFrom': '/talk/m/%s' % msgId,
            'ver': '1.0',
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/copy.nhn', data=data)
        if r.status_code != 200:
            raise Exception('Forward object failure.')
        return True
    
    #Sometime fails,If send same gif multiple time.
    #Try to use with forwardObjectMsg.
    @loggedIn
    def sendGif(self, to, path,name='file'):
        import base64
        with open(path, "rb") as f:
            body = base64.b64encode(f.read())
        req_bytes = base64.b64decode(body)
        params = '{"reqseq":"0","cat":"original","range":"bytes 0-%s\/%s","oid":"reqseq","tomid":"%s","name":"%s.gif","quality":"80","ver":"1.0","type":"image"}' % (str(len(req_bytes)-1),str(len(req_bytes)),name,to)
        head={
            "Content-Type":"image/gif",
            "Connection":"Keep-Alive",
            "Accept": "*/*",
            "User-Agent": self.server.USER_AGENT,
            "X-Line-Access":self.authToken,
            "X-Line-Carrier": self.server.CARRIER,
            "x-obs-params": base64.b64encode(params.encode('utf-8')),
            "X-Line-Application": self.server.APP_NAME,
            "Content-Length": str(len(req_bytes))
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + "/r/talk/m/reqseq", data=req_bytes,headers=head)
        if r.status_code != 201:
            raise Exception('Update failure.')
        return True
        
    @loggedIn
    def sendGifWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGif(to, path)
        
    @loggedIn
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': objectId,
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    @loggedIn
    def sendImageWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage(to, path)

    @loggedIn
    def sendVideo(self, to, path):
        contentMetadata = {
            'VIDLEN' : '60000',
            'DURATION' : '60000'
        }
        objectId = self.sendMessage(to=to, text=None, contentMetadata=contentMetadata, contentType = 2).id
        files = {
            'file': open(path, 'rb')
        }
        params = {
            'name': 'media',
            'oid': objectId,
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    @loggedIn
    def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendVideo(to, path)

    @loggedIn
    def sendAudio(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 3).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': objectId,
            'size': len(open(path, 'rb').read()),
            'type': 'audio',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload audio failure.')
        return True

    @loggedIn
    def sendAudioWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendAudio(to, path)

    @loggedIn
    def sendFile(self, to, path, file_name=''):
        if file_name == '':
            import ntpath
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        contentMetadata = {
            'FILE_NAME' : str(file_name),
            'FILE_SIZE' : str(file_size)
        }
        objectId = self.sendMessage(to=to, text=None, contentMetadata=contentMetadata, contentType = 14).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': file_name,
            'oid': objectId,
            'size': file_size,
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload file failure.')
        return True

    @loggedIn
    def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendFile(to, path, fileName)
        
    """Development"""
    #These functions are still development. It doesn't works. if you have a working code please pull it on linepy GitHub Repo
    
    @loggedIn
    def postNote(self, gid, text):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel instance is required for acquire this action.')
        else:
            params = {"postInfo":{"readPermission":{"gids":gid}},"sourceType":"GROUPHOME","contents":{"text":text}}
            #endpoint was changed?
            r = self.server.postContent(self.server.LINE_TIMELINE_API+"/v23/post/create.json", data=json.dumps(params), headers=self.server.channelHeaders)
            if r.status_code != 201:
                raise Exception('Post failure.')
            return True
            
    @loggedIn
    def deleteAlbum(self,gid,albumId):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel instance is required for acquire this action.')
        else:
            #endpoint was changed?
            url = self.server.LINE_HOST_DOMAIN+"/mh/album/v3/album/"+albumId+"?homeId="+gid
            r = self.server.deleteContent(url, headers=self.server.channelHeaders)
            if r.status_code != 201:
                raise Exception('DeleteAlbum failure.')
            return True

    @loggedIn
    def changeAlbumName(self,gid,name,albumId):
        import requests
        payload = {
            "title": name
        }
        r = requests.put(
            #endpoint was changed?
            self.server.LINE_HOST_DOMAIN + "/mh/album/v3/album/" + albumId + "?homeId=" + gid,
            headers = self.server.channelHeaders,
            data = json.dumps(payload),
        )
        if r.status_code != 201:
            raise Exception('ChangeName failure.')
        return True
        
    @loggedIn
    def addImageToAlbum(self, gid, albumid, path):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel instance is required for acquire this action.')
        else:
            #need to set right ObjectId to here?
            oid = gid
            with open(path, "rb") as f:
                body = base64.b64encode(f.read())
            req_bytes = base64.b64decode(body)
            params = '{"quality":"90","ver":"1.0","type":"image","range":"bytes 0-%s\/%s","oid":"%s","name":"%s"}' % (str(len(req_bytes)-1),str(len(req_bytes)),oid, datetime.now().strftime('timeline_%Y%m%d_%H%M%S.jpg'))
            headers={
                "content-Type":"image/jpeg",
                "connection":"Keep-Alive",
                "accept": "*/*",
                "X-Line-ChannelToken": self.server.channelHeaders['X-LCT'],
                "X-Line-Album": str(albumid),
                "User-Agent": self.server.USER_AGENT,
                "x-obs-params": base64.b64encode(params.encode('utf-8')),
                "X-Line-Carrier": self.server.CARRIER,
                "X-Line-Application": self.server.APP_NAME,
                "X-Line-Mid": gid,
                "Content-Length": str(len(req_bytes))
            }
            r = self.server.postContent(self.server.LINE_OBS_DOMAIN + "/album/a/upload.nhn", data=data, headers=headers)
            if r.status_code != 201:
                raise Exception('Upload failure.')
            return True