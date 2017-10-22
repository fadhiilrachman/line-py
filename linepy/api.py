<<<<<<< HEAD
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
        self.server.setHeaders('User-Agent', self.server.USER_AGENT)
        self.server.setHeaders('X-Line-Application', self.server.APP_NAME)

    def loadSession(self):
        self._client    = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        self.poll       = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_POLL_QUERY_PATH_FIR).Talk()
        self.call       = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CALL_QUERY_PATH).Call()
        self.channel    = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CHAN_QUERY_PATH).Channel()
        
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True

    def login(self, _id, passwd, certificate=None, systemName=None, keepLoggedIn=True):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME
        if self.server.EMAIL_REGEX.match(_id):
            self.provider = IdentityProvider.LINE       # LINE
        else:
            self.provider = IdentityProvider.NAVER_KR   # NAVER
        
        self.server.setHeaders('X-Line-Application', self.server.PHONE_NAME)
        self.server.setHeaders('X-Line-Carrier', self.server.CARRIER)
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
                    self.tokenLogin(result.authToken)
                else:
                    return False
            else:
                raise Exception("Login failed")

        elif result.type == LoginResultType.REQUIRE_QRCODE:
            self.qrLogin(keepLoggedIn, systemName)
            pass

        elif result.type == LoginResultType.SUCCESS:
            self.certificate = result.certificate
            self.tokenLogin(result.authToken)

    def qrLogin(self, keepLoggedIn=True, systemName=None):
        if systemName is None:
            systemName=self.server.SYSTEM_NAME

        self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)
        qrCode = self._client.getAuthQrcode(keepLoggedIn, systemName)

        self.callback.QrUrl("line://au/q/" + qrCode.verifier, True)
        self.server.setHeaders('X-Line-Access', qrCode.verifier)

        getAccessKey = self.server.getJson(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)
        result = self._client.loginWithVerifierForCertificate( getAccessKey['result']['verifier'] )

        self.tokenLogin(result.authToken)

    def tokenLogin(self, authToken=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        self.server.setHeaders('X-Line-Access', authToken)
        self.authToken = authToken
        self.loadSession()

    def defaultCallback(self, str):
        print(str)

    def logout(self):
=======
# -*- coding: utf-8 -*-
from akad.ttypes import IdentityProvider
from .server import LineServer
from .session import LineSession
from .callback import LineCallback

import rsa, os

class LineApi(object):
    isLogin = False
    revision = None
    
    server = None
    call = None
    channel = None
    poll = None
    profile = None
    
    authToken = ""
    certificate = ""

    def __init__(self):
        self.server = LineServer()
        self.callback = LineCallback(self.defaultCallback)
        self.server.set_Headers('User-Agent', self.server.UserAgent)
        self.server.set_Headers('X-Line-Application', self.server.AppName)
        self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_AUTH_QUERY_PATH).Talk(isopen=False)

    def loadSession(self):
        self._client = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_API_QUERY_PATH_FIR).Talk()
        self.poll = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_POLL_QUERY_PATH_FIR).Talk()
        self.call = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CALL_QUERY_PATH).Call()
        self.channel = LineSession(self.server.LINE_HOST_DOMAIN, self.server.Headers, self.server.LINE_CHAN_QUERY_PATH).Channel()
        
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True

    def login(self, email, passwd, certificate=None, systemName=None):
        if systemName is None:
            systemName=self.server.SystemName
            
        session_json = self.server.get_json(self.server.parseUrl(self.server.LINE_SESSION_LINE_QUERY_PATH))

        self.server.set_Headers('X-Line-Application', self.server.AppName)

        session_key = session_json['session_key']
        message = (chr(len(session_key)) + session_key +
                   chr(len(email)) + email +
                   chr(len(passwd)) + passwd).encode('utf-8')

        keyname, n, e   = session_json['rsa_key'].split(",")
        pub_key         = rsa.PublicKey(int(n, 16), int(e, 16))
        crypto          = rsa.encrypt(message, pub_key).hex()

        try:
            with open(email + ".crt", 'r') as f:
                self.certificate = f.read()
        except:
            self.certificate = certificate
            if os.path.exists(certificate):
                with open(certificate, 'r') as f:
                    self.certificate = f.read()
            
        result = self._client.loginWithIdentityCredentialForCertificate(IdentityProvider.LINE, keyname, crypto, True, self.server.ip, systemName, self.certificate)
        
        if result.type == 3:
            self.server._pincode = result.pinCode

            self.callback.Pinverified(self.server._pincode)
            getAccessKey = self.server.get_json(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)

            self.verifier = getAccessKey['result']['verifier']

            result = self._client.loginWithVerifierForCerificate(self.verifier)

            if result.type == 1:
                if result.certificate is not None:
                    with open(email + ".crt", 'wb') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate
                if result.authToken is not None:
                    self.authToken = result.authToken
                    self.server.set_Headers('X-Line-Access', result.authToken)
                    self.loadSession()
                else:
                    return False
            else:
                raise Exception("Login failed")

        elif result.type == 2:
            raise Exception('Require QR Login method')
            pass

        elif result.type == 1:
            self.certificate = result.certificate
            self.authToken = result.authToken
            self.server.set_Headers('X-Line-Access', result.authToken)
            self.loadSession()

    def tokenLogin(self, authToken):
        self.server.set_Headers('X-Line-Access', authToken)
        self.authToken = authToken
        self.loadSession()

    def qrLogin(self, keepLoggedIn=True, systemName=None):
        if systemName is None:
            systemName=self.server.SystemName
            
        qr = self._client.getAuthQrcode(keepLoggedIn, systemName)

        self.callback.QrUrl("line://au/q/" + qr.verifier)

        self.server.set_Headers('X-Line-Application', self.server.AppName)
        self.server.set_Headers('X-Line-Access', qr.verifier)

        verified = self.server.get_json(self.server.parseUrl(self.server.LINE_CERTIFICATE_PATH), allowHeader=True)
        result = self._client.loginWithVerifierForCertificate( verified['result']['verifier'] )

        self.authToken = result.authToken
        self.server.set_Headers('X-Line-Access', self.authToken)
        self.loadSession()

    def defaultCallback(self, str):
        print(str)

    def logout(self):
>>>>>>> 9965d22e728aef2765228b3c149e500e6d16b7c3
        self._client.logoutSession(self.authToken)