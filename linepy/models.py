# -*- coding: utf-8 -*-
from akad.ttypes import Message
from datetime import datetime

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