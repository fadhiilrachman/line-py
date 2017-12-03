# -*- coding: utf-8 -*-
from datetime import datetime
import json, shutil, time, ntpath

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You must login to LINE')
    return checkLogin
    
class LineObject(object):

    def __init__(self):
        if self.isLogin == True:
            self.log("[%s] : Login success" % self.profile.displayName)

    """Group"""

    @loggedIn
    def updateGroupPicture(self, groupId, path):
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'oid': groupId,'type': 'image'})}
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/g/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update group picture failure.')
        return True

    """Personalize"""

    @loggedIn
    def updateProfilePicture(self, path, type='p'):
        files = {'file': open(path, 'rb')}
        params = {'oid': self.profile.mid,'type': 'image'}
        if type == 'vp':
            params.update({'ver': '2.0', 'cat': 'vp.mp4'})
        data = {'params': self.genOBSParams(params)}
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/p/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True
        
    @loggedIn
    def updateProfileVideoPicture(self, path):
        try:
            from ffmpy import FFmpeg
            files = {'file': open(path, 'rb')}
            data = {'params': self.genOBSParams({'oid': self.profile.mid,'ver': '2.0','type': 'video','cat': 'vp.mp4'})}
            r_vp = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/vp/upload.nhn', data=data, files=files)
            if r_vp.status_code != 201:
                raise Exception('Update profile video picture failure.')
            path_p = self.genTempFile('path')
            ff = FFmpeg(inputs={'%s' % path: None}, outputs={'%s' % path_p: ['-ss', '00:00:2', '-vframes', '1']})
            ff.run()
            self.updateProfilePicture(path_p, 'vp')
        except:
            raise Exception('You should install FFmpeg and ffmpy from pypi')

    # These function are still development. It doesn't works.
    # If you have a working code please pull it on linepy GitHub Repo
    @loggedIn
    def updateProfileCover(self, path):
        if len(self.server.channelHeaders) < 1:
            raise Exception('LineChannel instance is required for acquire this action.')
        else:
            home = self._channel.getProfileDetail(self.profile.mid)
            oldObjId, objId = home["result"]["objectId"], int(time.time())
            file = open(path, 'rb').read()
            params = {
                'userid': '%s' % self.profile.mid,
                'oid': '%s' % str(objId),
                'range': len(file),
                'type': 'image'
            }
            hr = self.server.additionalHeaders(self.server.channelHeaders, {
                'Content-Type': 'image/jpeg',
                'Content-Length': str(len(file)),
                'x-obs-params': self.genOBSParams(params,'b64')
            })
            r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/myhome/c/upload.nhn', headers=hr, data=file)
            if r.status_code != 201:
                raise Exception('Update profile cover failure.')
            return True

    """Object"""

    @loggedIn
    def downloadObjectMsg(self, messageId, returnAs='path', saveAs=''):
        if saveAs == '':
            saveAs = self.genTempFile('path')
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
        data = self.genOBSParams({'oid': 'reqseq','reqseq': self.revision,'type': contentType,'copyFrom': '/talk/m/%s' % msgId},'default')
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/copy.nhn', data=data)
        if r.status_code != 200:
            raise Exception('Forward object failure.')
        return True

    @loggedIn
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'oid': objectId,'size': len(open(path, 'rb').read()),'type': 'image'})}
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    @loggedIn
    def sendImageWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage(to, path)

    @loggedIn
    def sendGIF(self, to, path):
        file = open(path, 'rb').read()
        params = {
            'oid': 'reqseq',
            'reqseq': '%s' % str(self.revision),
            'tomid': '%s' % str(to),
            'size': '%s' % str(len(file)),
            'range': len(file),
            'type': 'image'
        }
        hr = self.server.additionalHeaders(self.server.Headers, {
            'Content-Type': 'image/gif',
            'x-obs-params': self.genOBSParams(params,'b64')
        })
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/r/talk/m/reqseq', data=file, headers=hr)
        if r.status_code != 201:
            raise Exception('Upload GIF failure.')
        return True

    @loggedIn
    def sendGIFWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGIF(to, path)

    @loggedIn
    def sendVideo(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2).id
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'oid': objectId,'size': len(open(path, 'rb').read()),'type': 'video'})}
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
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'oid': objectId,'size': len(open(path, 'rb').read()),'type': 'audio'})}
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
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(file_size)}, contentType = 14).id
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'name': file_name,'oid': objectId,'size': file_size,'type': 'file'})}
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload file failure.')
        return True

    @loggedIn
    def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendFile(to, path, fileName)