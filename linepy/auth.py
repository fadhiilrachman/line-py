# -*- coding: utf-8 -*-
from akad.ttypes import IdentityProvider, LoginResultType, LoginRequest, LoginType
from .server import Server
from .session import Session
from .callback import Callback

import rsa, os

class Auth(object):
    isLogin     = False
    authToken   = ""
    certificate = ""

    def __init__(self):
        self.server = Server()
        self.callback = Callback(self.__defaultCallback)
        self.server.setHeadersWithDict({
            'User-Agent': self.server.USER_AGENT,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-Carrier': self.server.CARRIER
        })

    def __loadSession(self):
        self.talk       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        self.poll       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_POLL_QUERY_PATH_FIR).Talk()
        self.call       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CALL_QUERY_PATH).Call()
        self.channel    = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CHAN_QUERY_PATH).Channel()
        self.square     = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_SQUARE_QUERY_PATH).Square()
        self.shop       = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_SHOP_QUERY_PATH).Shop()
        
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True

    def __loginRequest(self, type, data):
        lReq = LoginRequest()
        if type == '0':
            lReq.type = LoginType.ID_CREDENTIAL
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = LoginType.QRCODE
            lReq.keepLoggedIn = data['keepLoggedIn']
            if 'identityProvider' in data:
                lReq.identityProvider = data['identityProvider']
            if 'accessLocation' in data:
                lReq.accessLocation = data['accessLocation']
            if 'systemName' in data:
                lReq.systemName = data['systemName']
            lReq.verifier = data['verifier']
            lReq.e2eeVersion = data['e2eeVersion']
        else:
            lReq=False
        return lReq

    def loginWithCredential(self, _id, passwd, certificate=None, systemName=None, appName=None, keepLoggedIn=True):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME
        if self.server.EMAIL_REGEX.match(_id):
            self.provider = IdentityProvider.LINE       # LINE
        else:
            self.provider = IdentityProvider.NAVER_KR   # NAVER
        
        if appName is None:
            appName=self.server.APP_NAME
        self.server.setHeaders('X-Line-Application', appName)
        self.tauth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)

        rsaKey = self.tauth.getRSAKeyInfo(self.provider)
        
        message = (chr(len(rsaKey.sessionKey)) + rsaKey.sessionKey +
                   chr(len(_id)) + _id +
                   chr(len(passwd)) + passwd).encode('utf-8')
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16), int(rsaKey.evalue, 16))
        crypto = rsa.encrypt(message, pub_key).hex()

        try:
            with open(_id + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if certificate is not None:
                self.certificate = certificate
                if os.path.exists(certificate):
                    with open(certificate, 'r') as f:
                        self.certificate = f.read()

        self.auth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

        lReq = self.__loginRequest('0', {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': keepLoggedIn,
            'accessLocation': self.server.IP_ADDR,
            'systemName': systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })

        result = self.auth.loginZ(lReq)
        
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            self.callback.PinVerified(result.pinCode)

            self.server.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)

            self.auth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

            try:
                lReq = self.__loginRequest('1', {
                    'keepLoggedIn': keepLoggedIn,
                    'verifier': getAccessKey['result']['verifier'],
                    'e2eeVersion': 0
                })
                result = self.auth.loginZ(lReq)
            except:
                raise Exception('Login failed')
            
            if result.type == LoginResultType.SUCCESS:
                if result.certificate is not None:
                    with open(_id + '.crt', 'w') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate
                if result.authToken is not None:
                    self.loginWithAuthToken(result.authToken, appName)
                else:
                    return False
            else:
                raise Exception('Login failed')

        elif result.type == LoginResultType.REQUIRE_QRCODE:
            self.loginWithQrCode(keepLoggedIn, systemName, appName)
            pass

        elif result.type == LoginResultType.SUCCESS:
            self.certificate = result.certificate
            self.loginWithAuthToken(result.authToken, appName)

    def loginWithQrCode(self, keepLoggedIn=True, systemName=None, appName=None, showQr=False):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME
        if appName is None:
            appName=self.server.APP_NAME
        self.server.setHeaders('X-Line-Application', appName)

        self.tauth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)
        qrCode = self.tauth.getAuthQrcode(keepLoggedIn, systemName)

        self.callback.QrUrl('line://au/q/' + qrCode.verifier, showQr)
        self.server.setHeaders('X-Line-Access', qrCode.verifier)

        getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)
        
        self.auth = Session(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)
        
        try:
            lReq = self.__loginRequest('1', {
                'keepLoggedIn': keepLoggedIn,
                'systemName': systemName,
                'identityProvider': IdentityProvider.LINE,
                'verifier': getAccessKey['result']['verifier'],
                'accessLocation': self.server.IP_ADDR,
                'e2eeVersion': 0
            })
            result = self.auth.loginZ(lReq)
        except:
            raise Exception('Login failed')

        if result.type == LoginResultType.SUCCESS:
            if result.authToken is not None:
                self.loginWithAuthToken(result.authToken, appName)
            else:
                return False
        else:
            raise Exception('Login failed')

    def loginWithAuthToken(self, authToken=None, appName=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        if appName is None:
            appName=self.server.APP_NAME
        self.server.setHeadersWithDict({
            'X-Line-Application': appName,
            'X-Line-Access': authToken
        })
        self.authToken = authToken
        self.__loadSession()

    def __defaultCallback(self, str):
        print(str)

    def logout(self):
        self.auth.logoutZ()