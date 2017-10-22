# -*- coding: utf-8 -*-
<<<<<<< HEAD
from datetime import datetime
from random import randint

import json, shutil, tempfile
=======
from akad.ttypes import Message
from datetime import datetime

import json, shutil
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3

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

<<<<<<< HEAD
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
=======
    """Object"""

    @loggedIn
    def downloadObjectMsgId(self, path, messageId, extension='data'):
        path_n = '%s/%s.%s' % (path, messageId, extension)
        url = self.server.LINE_OBS_DOMAIN + '/talk/m/download.nhn?oid=%s' % messageId
        r = self.server.get_content(url)
        if r.status_code == 200:
            with open(path_n, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            return True
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        else:
            raise Exception('Download object failure.')
        
    @loggedIn
<<<<<<< HEAD
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
=======
    def sendImage(self, to_, path):
        M = Message(to=to_, text=None, contentType = 1)
        M.contentMetadata = None
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
<<<<<<< HEAD
            'oid': objectId,
=======
            'oid': M_id,
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
<<<<<<< HEAD
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
=======
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

    @loggedIn
<<<<<<< HEAD
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
=======
    def sendVideo(self, to_, path):
        M = Message(to=to_, text=None, contentType = 2)
        M.contentMetadata = {
            'VIDLEN' : '60000',
            'DURATION' : '60000'
        }
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        files = {
            'file': open(path, 'rb')
        }
        params = {
            'name': 'media',
<<<<<<< HEAD
            'oid': objectId,
=======
            'oid': M_id,
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
<<<<<<< HEAD
        r = self.server.postContent(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
=======
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

    @loggedIn
<<<<<<< HEAD
    def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(self, url, returnAs='path')
        try:
            return self.sendVideo(to, path)
        except:
            raise Exception('Send video failure.')

    @loggedIn
    def sendAudio(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 3).id
=======
    def sendVoice(self, to_, path):
        M = Message(to=to_, text=None, contentType = 3)
        M.contentPreview = None
        M_id = self._client.sendMessage(0,M).id
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        files = {
            'file': open(path, 'rb'),
        }
        params = {
<<<<<<< HEAD
            'name': 'media',
            'oid': objectId,
=======
            'name': 'voice_message',
            'oid': M_id,
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
            'size': len(open(path, 'rb').read()),
            'type': 'audio',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
<<<<<<< HEAD
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
=======
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
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': file_name,
<<<<<<< HEAD
            'oid': objectId,
=======
            'oid': M_id,
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
            'size': file_size,
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
<<<<<<< HEAD
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
=======
        r = self.server.post_content(self.server.LINE_OBS_DOMAIN + '/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload file failure.')
        return True
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
