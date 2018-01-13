# -*- coding: utf-8 -*-
from akad.ttypes import *

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You want to call the function, you must login to LINE")
    return checkLogin

class LineSquare(object):
    isLogin = False

    def __init__(self):
        self.isLogin = True
        
    @loggedIn
    def searchSquareMembers(self, squareMid, continuationToken=None, limit=50):
        rq = SearchSquareMembersRequest()
        rq.squareMid = squareMid
        rq.searchOption = SquareMemberSearchOption()
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.searchSquareMembers(rq)
        
    @loggedIn
    def findSquareByInvitationTicket(self, invitationTicket):
        rq = FindSquareByInvitationTicketRequest()
        rq.invitationTicket = invitationTicket
        return self.square.findSquareByInvitationTicket(rq)
        
    @loggedIn
    def approveSquareMembers(self, squareMid, requestedMemberMids=[]):
        rq = ApproveSquareMembersRequest()
        rq.squareMid = squareMid
        rq.requestedMemberMids = requestedMemberMids
        return self.square.approveSquareMembers(rq)
        
    @loggedIn
    def destroySquareMessage(self, squareChatMid, messageId):
        rq = DestroyMessageRequest()
        rq.squareChatMid = squareChatMid
        rq.messageId = messageId
        return self.square.destroyMessage(rq)
        
    @loggedIn
    def deleteSquare(self, mid):
        rq = DeleteSquareRequest()
        rq.mid = mid
        rq.revision = self.client.revision
        return self.square.deleteSquare(rq)

    @loggedIn
    def deleteSquareChat(self, squareChatMid):
        rq = DeleteSquareChatRequest()
        rq.squareChatMid = squareChatMid
        rq.revision = self.client.revision
        return self.square.deleteSquareChat(request)
        
    @loggedIn
    def createSquare(self, name, categoryID, welcomeMessage='', profileImageObsHash='', desc='', searchable=True, type=1, ableToUseInvitationTicket=True):
        rq = CreateSquareRequest()
        rq.square = Square()
        rq.square.name = name
        rq.square.categoryID = categoryID
        rq.square.welcomeMessage = welcomeMessage
        rq.square.profileImageObsHash = profileImageObsHash
        rq.square.desc = desc
        rq.square.searchable = searchable
        rq.square.type = type
        rq.square.ableToUseInvitationTicket = ableToUseInvitationTicket
        rq.creator = SquareMember()
        return self.square.createSquare(rq)
        
    @loggedIn
    def createSquareChat(self, squareMid, name, squareMemberMids):
        rq = CreateSquareChatRequest()
        rq.reqSeq = self.client.revision
        rq.squareChat = SquareChat()
        rq.squareChat.squareMid = squareMid
        rq.squareChat.name = name
        rq.squareMemberMids = squareMemberMids
        return self.square.createSquareChat(request)
        
    @loggedIn
    def fetchSquareChatEvents(self, squareChatMid, syncToken, limit=50, direction=2):
        rq = FetchSquareChatEventsRequest()
        rq.subscriptionId = subscriptionId
        rq.squareChatMid = squareChatMid
        rq.syncToken = syncToken
        rq.limit = limit
        rq.direction = direction
        return self.square.fetchSquareChatEvents(rq)
        
    @loggedIn
    def getSquare(self, mid):
        return self.square.getSquare(mid)
        
    @loggedIn
    def sendSquareMessage(self, squareChatMid, text, contentMetadata={}, contentType=0):
        rq = SendMessageRequest()
        rq.squareChatMid = squareChatMid
        rq.squareMessage = SquareMessage()
        msg = Message()
        msg.to = squareChatMid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        rq.squareMessage.message = msg
        rq.squareMessage.fromType = 4
        if to not in self.client._messageReq:
            self.client._messageReq[to] = -1
        self.client._messageReq[to] += 1
        rq.squareMessage.squareMessageRevision = self.client._messageReq[to]
        return self.square.sendMessage(rq)

    @loggedIn
    def getJoinedSquares(self, continuationToken=None, limit=50):
        rq = GetJoinedSquaresRequest()
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getJoinedSquares(rq)