<<<<<<< HEAD
# -*- coding: utf-8 -*-
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from akad import TalkService, ChannelService, CallService

class LineSession:

    def __init__(self, url, headers, path=''):
        self.host = url + path
        self.headers = headers

    def Talk(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._talk  = TalkService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._talk

    def Channel(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._channel  = ChannelService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._channel

    def Call(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._call  = CallService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._call
=======
# -*- coding: utf-8 -*-
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from akad import TalkService, ChannelService, CallService

class LineSession:
    host = None
    headers = None
    transport = None
    protocol = None
    
    _client = None

    def __init__(self, url, headers, path=''):
        self.host = url + path
        self.headers = headers

    def Talk(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = TalkService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client

    def Channel(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = ChannelService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client

    def Call(self, isopen=True):
        self.transport = THttpClient.THttpClient(self.host)
        self.transport.setCustomHeaders(self.headers)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self._client  = CallService.Client(self.protocol)
        
        if isopen:
            self.transport.open()

        return self._client
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
