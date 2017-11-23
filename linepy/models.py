# -*- coding: utf-8 -*-
from datetime import datetime
from .object import LineObject
from random import randint

import json, shutil, time, os, base64, tempfile
    
class LineModels(LineObject):

    _channel    = None
        
    def __init__(self):
        LineObject.__init__(self)

    def setChannelToModels(self, channel):
        self._channel = channel

    """Text"""

    def log(self, text):
        print("[%s] %s" % (str(datetime.now()), text))

    """File"""

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False

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

    """Generator"""

    def genTempFileName(self):
        try:
            return '%s/linepy-%s-%i.bin' % (tempfile.gettempdir(), int(time.time()), randint(0, 9))
        except:
            raise Exception('tempfile is required')

    def genOBSParams(self, newList, returnAs='json'):
        oldList = {'name': 'media','cat': 'original','ver': '1.0'}
        if returnAs not in ['json','default']:
            raise Exception('Invalid parameter returnAs')
        oldList.update(newList)
        if returnAs == 'json':
            return json.dumps(oldList)
        elif returnAs == 'default':
            return oldList

    def genOBSParamsB64(self, newList, returnAs='b64'):
        oldList = {'name': 'media','cat': 'original','ver': '1.0'}
        if returnAs not in ['b64','json']:
            raise Exception('Invalid parameter returnAs')
        oldList.update(newList)
        if returnAs == 'json':
            return json.dumps(oldList)
        elif returnAs == 'b64':
            oldList=json.dumps(oldList).replace('[-]', '\/')
            oldList=base64.b64encode(oldList.encode('utf-8'))
            return oldList
