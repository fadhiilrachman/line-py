# -*- coding: utf-8 -*-
class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def PinVerified(self, pin):
        self.callback("Input this PIN code '" + pin + "' on your LINE for smartphone in 2 minutes")

    def QrUrl(self, url, showQr=True):
        self.callback("Open this link or scan this QR on your LINE for smartphone in 2 minutes\n" + url)
        if showQr:
            import pyqrcode
            url = pyqrcode.create(url)
            self.callback(url.terminal('green', 'white', 1))

    def default(self, str):
        self.callback(str)