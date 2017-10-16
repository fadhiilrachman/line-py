# -*- coding: utf-8 -*-
import json, requests

class LineServer(object):
    LINE_HOST_DOMAIN = 'https://gd2.line.naver.jp'
    LINE_OBS_DOMAIN = 'https://obs.line-apps.com'

    LINE_AUTH_QUERY_PATH            = '/api/v4/TalkService.do'
    LINE_SESSION_LINE_QUERY_PATH    = '/authct/v1/keys/line'
    LINE_SESSION_NAVER_QUERY_PATH   = '/authct/v1/keys/naver'

    LINE_API_QUERY_PATH_FIR         = '/S4'
    LINE_POLL_QUERY_PATH_FIR        = '/P4'
    LINE_CALL_QUERY_PATH            = '/V4'
    LINE_CERTIFICATE_PATH           = '/Q'
    LINE_CHAN_QUERY_PATH            = '/CH4'

    UserAgent   = 'Line/7.5.2 iPad4,1 9.0.2'
    AppName     = 'IOSIPAD 7.5.2 iPhone OS 9.0.2'
    port        = 443
    SystemName  = 'FDLRCN'
    ip          = '127.0.0.1'
    _session = requests.session()
    channelHeaders={}
    Headers = {}
    _pincode = None

    def parseUrl(self, path):
        return self.LINE_HOST_DOMAIN + path

    def get_json(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.Headers).text)

    def set_Headers(self, argument, value):
        self.Headers[argument] = value

    def set_channelHeaders(self, argument, value):
        self.channelHeaders[argument] = value

    def post_content(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.post(url, headers=headers, data=data, files=files)

    def get_content(self, url, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.get(url, headers=headers, stream=True)