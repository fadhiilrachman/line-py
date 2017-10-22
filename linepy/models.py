# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint

import json, shutil, tempfile

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

    """Personalize"""

    @loggedIn
    def updateProfilePicture(self, hash_id):
        return self.updateProfileAttribute(8, hash_id)
    
    @loggedIn
    def cloneContactProfile(self, mid):
        contact = self.getContact(mid)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        profile.pictureStatus = contact.pictureStatus
        self.updateProfilePicture(profile.pictureStatus)
        return self.updateProfile(profile)

    """Object"""

    def downloadFileURL(self, fileUrl, returnAs='path', saveAs=''):
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        if saveAs == '':
            saveAs = '%s/linepy-%i.data' % (tempfile.gettempdir(), randint(0, 9))
        r = self.server.getContent(fileUrl)
        if r.status_code == 200:
            if returnAs in ['path','bool']:
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
    def downloadObjectMsgId(self, path, messageId, returnAs='path', saveAs=''):
        if saveAs == '':
            saveAs = '%s/%s-%i.bin' % (tempfile.gettempdir(), messageId, randint(0, 9))
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        params = {'oid': messageId}
        url = self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/talk/m/download.nhn', params)
        r = self.server.getContent(url)
        if r.status_code == 200:
            if returnAs in ['path','bool']:
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
        path = self.downloadFileURL(self, url, returnAs='path')
        try:
            return self.sendImage(to, path)
        except:
            raise Exception('Send image failure.')

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
        path = self.downloadFileURL(self, url, returnAs='path')
        try:
            return self.sendVideo(to, path)
        except:
            raise Exception('Send video failure.')

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
        path = self.downloadFileURL(self, url, returnAs='path')
        try:
            return self.sendAudio(to, path)
        except:
            raise Exception('Send audio failure.')

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
        path = self.downloadFileURL(self, url, returnAs='path')
        try:
            return self.sendFile(to, path, fileName)
        except:
            raise Exception('Send file failure.')