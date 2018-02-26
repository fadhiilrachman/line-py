# -*- coding: utf-8 -*-
from datetime import datetime
from .object import Object
from random import randint

import json
import shutil
import time
import os
import base64
import tempfile


class Models(Object):

    def __init__(self):
        Object.__init__(self)

    """Text"""

    def log(self, text):
        print("[%s] %s" % (str(datetime.now()), text))

    """File"""

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False

    def downloadFileURL(self, fileUrl, returnAs='path',
                        saveAs='', headers=None):
        if returnAs not in ['path', 'bool', 'bin']:
            raise Exception('Invalid returnAs value')
        if saveAs == '':
            saveAs = self.genTempFile()
        r = self.server.getContent(fileUrl, headers=headers)
        if r.status_code != 404:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download file failure.')

    """Generator"""

    def genTempFile(self, returnAs='path'):
        try:
            if returnAs not in ['file', 'path']:
                raise Exception('Invalid returnAs value')
            fName = 'linepy-%s-%i.bin' % (int(time.time()), randint(0, 9))
            fPath = tempfile.gettempdir()
            if returnAs == 'file':
                return fName
            elif returnAs == 'path':
                return os.path.join(fPath, fName)
        except:
            raise Exception('tempfile is required')

    def genOBSParams(self, newList, returnAs='json'):
        oldList = {'name': self.genTempFile('file'), 'ver': '1.0'}
        if returnAs not in ['json', 'b64', 'default']:
            raise Exception('Invalid parameter returnAs')
        oldList.update(newList)
        if 'range' in oldList:
            new_range = 'bytes 0-%s\/%s' % (str(oldList['range'] - 1),
                                            str(oldList['range']))
            oldList.update({'range': new_range})
        if returnAs == 'json':
            oldList = json.dumps(oldList)
            return oldList
        elif returnAs == 'b64':
            oldList = json.dumps(oldList)
            return base64.b64encode(oldList.encode('utf-8'))
        elif returnAs == 'default':
            return oldList
