# -*- coding: utf-8 -*-
from akad.ttypes import IdentityProvider, LoginResultType
from .server import LineServer
from .session import LineSession
from .callback import LineCallback

import rsa, os

class LineApi(object):
    isLogin     = False
    authToken   = ""
    certificate = ""

    def __init__(self):
        self.server = LineServer()
        self.callback = LineCallback(self.defaultCallback)
        self.server.setHeadersWithDict({
            'User-Agent': self.server.USER_AGENT,
            'X-Line-Application': self.server.APP_NAME,
            'X-Line-Carrier': self.server.CARRIER
        })

    def loadSession(self):
        self._client    = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        self.poll       = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_POLL_QUERY_PATH_FIR).Talk()
        self.call       = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CALL_QUERY_PATH).Call()
        self.channel    = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CHAN_QUERY_PATH).Channel()
        #self.square    = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_SQUARE_QUERY_PATH).Square()
        
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True

    def login(self, _id, passwd, certificate=None, systemName=None, phoneName=None, keepLoggedIn=True):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME
        if self.server.EMAIL_REGEX.match(_id):
            self.provider = IdentityProvider.LINE       # LINE
        else:
            self.provider = IdentityProvider.NAVER_KR   # NAVER
        
        if phoneName is None:
            phoneName=self.server.APP_NAME
        self.server.setHeaders('X-Line-Application', phoneName)
        self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)

        rsaKey = self._client.getRSAKeyInfo(self.provider)
        
        message = (chr(len(rsaKey.sessionKey)) + rsaKey.sessionKey +
                   chr(len(_id)) + _id +
                   chr(len(passwd)) + passwd).encode('utf-8')
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16), int(rsaKey.evalue, 16))
        try:
            # Works with python 2.7
            crypto = rsa.encrypt(message, pub_key).encode('hex')
        except:
            # Works with python 3.x
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
        
        result = self._client.loginWithIdentityCredentialForCertificate(
            self.provider, rsaKey.keynm, crypto, keepLoggedIn, self.server.IP_ADDR, systemName, self.certificate
        )
        
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            self.callback.PinVerified(result.pinCode)

            self.server.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)

            self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)
            try:
                result = self._client.loginWithVerifierForCertificate(getAccessKey['result']['verifier'])
            except:
                raise Exception("Login failed")
            
            if result.type == LoginResultType.SUCCESS:
                if result.certificate is not None:
                    with open(_id + '.crt', 'w') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate
                if result.authToken is not None:
                    self.tokenLogin(result.authToken, phoneName)
                else:
                    return False
            else:
                raise Exception("Login failed")

        elif result.type == LoginResultType.REQUIRE_QRCODE:
            self.qrLogin(keepLoggedIn, systemName, phoneName)
            pass

        elif result.type == LoginResultType.SUCCESS:
            self.certificate = result.certificate
            self.tokenLogin(result.authToken, phoneName)

    def qrLogin(self, keepLoggedIn=True, systemName=None, appName=None, showQr=False):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME
        if appName is None:
            appName=self.server.APP_NAME
        self.server.setHeaders('X-Line-Application', appName)

        self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)
        qrCode = self._client.getAuthQrcode(keepLoggedIn, systemName)

        self.callback.QrUrl("line://au/q/" + qrCode.verifier, showQr)
        self.server.setHeaders('X-Line-Access', qrCode.verifier)

        getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)
        result = self._client.loginWithVerifierForCertificate( getAccessKey['result']['verifier'] )

        self.tokenLogin(result.authToken, appName)

    def tokenLogin(self, authToken=None, appOrPhoneName=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        if appOrPhoneName is None:
            appOrPhoneName=self.server.APP_NAME
        self.server.setHeadersWithDict({
            'X-Line-Application': appOrPhoneName,
            'X-Line-Access': authToken
        })
        self.authToken = authToken
        self.loadSession()

    def defaultCallback(self, str):
        print(str)

    def logout(self):
        self._client.logoutSession(self.authToken)