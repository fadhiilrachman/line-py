# -*- coding: utf-8 -*-
class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def Pinverified(self, pin):
        self.callback("Input this PIN code '" + pin + "' on your LINE for smartphone in 2 minutes")

    def QrUrl(self, url):
        self.callback("Open this link on your LINE for smartphone in 2 minutes\n" + url)

    def default(self, str):
        self.callback(str)