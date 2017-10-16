# -*- coding: utf-8 -*-
from akad.ttypes import Message
from .api import LineApi
from .models import LineModels
from random import randint

import json

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin

class LineClient(LineApi, LineModels):

    def __init__(self, email=None, passwd=None, authToken=None, certificate=None, keepLoggedIn=True, systemName=None):
        LineApi.__init__(self)
        if not (authToken or email and passwd):
            self.qrLogin(keepLoggedIn=keepLoggedIn, systemName=systemName)
        if authToken:
            self.tokenLogin(authToken=authToken)
        if email and passwd:
            self.login(email=email, passwd=passwd, certificate=certificate, systemName=systemName)
        LineModels.__init__(self)

        self._messageReq = {}
        self.profile = self._client.getProfile()
        self.isLogin = True
        if self.isLogin == True:
            self.log("[%s] : Login success" % self.profile.displayName)

    """User"""

    @loggedIn
    def getProfile(self):
        return self._client.getProfile()

    @loggedIn
    def getSettings(self):
        return self._client.getSettings()

    @loggedIn
    def getUserTicket(self):
        return self._client.getUserTicket()

    @loggedIn
    def updateProfile(self, profileObject):
        return self._client.updateProfile(0, profileObject)

    @loggedIn
    def updateSettings(self, settingObject):
        return self._client.updateSettings(0, settingObject)

    """Operation"""

    @loggedIn
    def fetchOperation(self, revision, count):
        return self._client.fetchOperations(revision, count)

    @loggedIn
    def getLastOpRevision(self):
        return self._client.getLastOpRevision()

    """Message"""

    @loggedIn
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self._client.sendMessage(self._messageReq[to], msg)
        
    @loggedIn
    def sendMessageWithMention(self, to, text='', data=[]):
        arr = []
        list_text=''
        if '[list]' in text.lower():
            i=0
            for l in data:
                list_text+='\n@[list-'+str(i)+']'
                i=i+1
            text=text.replace('[list]', list_text)
        elif '[list-' in text.lower():
            text=text
        else:
            i=0
            for l in data:
                list_text+=' @[list-'+str(i)+']'
                i=i+1
            text=text+list_text
        i=0
        for l in data:
            mid=l[0]
            name='@[list-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            length_n=len(name)
            if ln_text.find(name):
                line_s=int( ln_text.index(name) )
                line_e=(int(line_s)+int(length_n))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        return self.sendMessage(to, text, contentMetadata)
        
    @loggedIn
    def removeMessage(self, messageId):
        return self._client.removeMessage(messageId)
        
    @loggedIn
    def removeAllMessages(self, lastMessageId):
        return self._client.removeAllMessages(0, lastMessageId)
        
    @loggedIn
    def sendChatChecked(self, consumer, messageId):
        return self._client.sendChatChecked(0, consumer, messageId)

    @loggedIn
    def sendEvent(self, messageObject):
        return self._client.sendEvent(0, messageObject)

    @loggedIn
    def getLastReadMessageIds(self, chatId):
        return self._client.getLastReadMessageIds(0,chatId)

    """Contact"""
        
    @loggedIn
    def blockContact(self, mid):
        return self._client.blockContact(0, mid)

    @loggedIn
    def unblockContact(self, mid):
        return self._client.unblockContact(0, mid)

    @loggedIn
    def findAndAddContactsByMid(self, mid):
        return self._client.findAndAddContactsByMid(0, mid)

    @loggedIn
    def findAndAddContactsByUserid(self, userid):
        return self._client.findAndAddContactsByUserid(0, userid)

    @loggedIn
    def findContactsByUserid(self, userid):
        return self._client.findContactByUserid(userid)

    @loggedIn
    def findContactByTicket(self, ticketId):
        return self._client.findContactByUserTicket(ticketId)

    @loggedIn
    def getAllContactIds(self):
        return self._client.getAllContactIds()

    @loggedIn
    def getBlockedContactIds(self):
        return self._client.getBlockedContactIds()

    @loggedIn
    def getContact(self, mid):
        return self._client.getContact(mid)

    @loggedIn
    def getContacts(self, midlist):
        return self._client.getContacts(midlist)

    @loggedIn
    def getFavoriteMids(self):
        return self._client.getFavoriteMids()

    @loggedIn
    def getHiddenContactMids(self):
        return self._client.getHiddenContactMids()

    @loggedIn
    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self._client.reissueUserTicket(expirationTime, maxUseCount)

    """Group"""
    
    @loggedIn
    def findGroupByTicket(self, ticketId):
        return self._client.findGroupByTicket(ticketId)

    @loggedIn
    def acceptGroupInvitation(self, groupId):
        return self._client.acceptGroupInvitation(0, groupId)

    @loggedIn
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self._client.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @loggedIn
    def cancelGroupInvitation(self, groupId, contactIds):
        return self._client.cancelGroupInvitation(0, groupId, contactIds)

    @loggedIn
    def createGroup(self, name, midlist):
        return self._client.createGroup(0, name, midlist)

    @loggedIn
    def getGroup(self, groupId):
        return self._client.getGroup(groupId)

    @loggedIn
    def getGroups(self, groupIds):
        return self._client.getGroups(groupIds)

    @loggedIn
    def getGroupIdsInvited(self):
        return self._client.getGroupIdsInvited()

    @loggedIn
    def getGroupIdsJoined(self):
        return self._client.getGroupIdsJoined()

    @loggedIn
    def inviteIntoGroup(self, groupId, midlist):
        return self._client.inviteIntoGroup(0, groupId, midlist)

    @loggedIn
    def kickoutFromGroup(self, groupId, midlist):
        return self._client.kickoutFromGroup(0, groupId, midlist)

    @loggedIn
    def leaveGroup(self, groupId):
        return self._client.leaveGroup(0, groupId)

    @loggedIn
    def rejectGroupInvitation(self, groupId):
        return self._client.rejectGroupInvitation(0, groupId)

    @loggedIn
    def reissueGroupTicket(self, groupId):
        return self._client.reissueGroupTicket(groupId)

    @loggedIn
    def updateGroup(self, groupObject):
        return self._client.updateGroup(0, groupObject)

    """Room"""

    @loggedIn
    def createRoom(self, midlist):
        return self._client.createRoom(0, midlist)

    @loggedIn
    def getRoom(self, roomId):
        return self._client.getRoom(roomId)

    @loggedIn
    def inviteIntoRoom(self, roomId, midlist):
        return self._client.inviteIntoRoom(0, roomId, midlist)

    @loggedIn
    def leaveRoom(self, roomId):
        return self._client.leaveRoom(0, roomId)

    """Call"""
        
    @loggedIn
    def acquireCallRoute(self, to):
        return self._client.acquireCallRoute(to)

    """Personalize"""
    
    @loggedIn
    def cloneContactProfile(self, mid):
        contact = self.getContact(mid)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        profile.pictureStatus = contact.pictureStatus
        self.updateProfilePicture(profile.pictureStatus)
        return self.updateProfile(profile)

    @loggedIn
    def updateProfilePicture(self, hash_id):
        return self._client.updateProfileAttribute(0, 8, hash_id)