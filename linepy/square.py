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
    def fetchSquareChatEvents(self, subscriptionId, squareChatMid, syncToken=None, limit=50, direction=2):
        rq = FetchSquareChatEventsRequest()
        rq.subscriptionId = subscriptionId
        rq.squareChatMid = squareChatMid
        rq.syncToken = syncToken
        rq.limit = limit
        rq.direction = direction
        return self.square.fetchSquareChatEvents(rq)
        
    @loggedIn
    def fetchMyEvents(self, subscriptionId, syncToken=None, continuationToken=None, limit=50):
        rq = FetchMyEventsRequest()
        rq.subscriptionId = subscriptionId
        rq.syncToken = syncToken
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.fetchMyEvents(rq)
        
    @loggedIn
    def markAsRead(self, squareChatMid, messageId):
        rq = MarkAsReadRequest()
        rq.squareChatMid = squareChatMid
        rq.messageId = messageId
        return self.square.markAsRead(rq)
        
    @loggedIn
    def getSquareAuthority(self, squareMid):
        rq = GetSquareAuthorityRequest()
        rq.squareMid = squareMid
        return self.square.getSquareAuthority(rq)

    @loggedIn
    def leaveSquare(self, squareMid):
        rq = LeaveSquareRequest()
        rq.squareMid = squareMid
        return self.square.leaveSquare(rq)

    @loggedIn
    def leaveSquareChat(self, squareChatMid, squareChatMemberRevision, sayGoodbye=False):
        rq = LeaveSquareChatRequest()
        rq.squareChatMid = squareChatMid
        rq.sayGoodbye = sayGoodbye
        rq.squareChatMemberRevision = squareChatMemberRevision
        return self.square.leaveSquareChat(rq)
        
    @loggedIn
    def joinSquareChat(self, squareChatMid):
        rq = JoinSquareChatRequest()
        rq.squareChatMid = squareChatMid
        return self.square.joinSquareChat(rq)
        
    @loggedIn
    def joinSquare(self, squareMid, displayName, profileImageObsHash):
        rq = JoinSquareRequest()
        rq.squareMid = squareMid
        rq.member = SquareMember()
        rq.member.squareMid = squareMid
        rq.member.displayName = displayName
        rq.member.profileImageObsHash = profileImageObsHash
        return self.square.joinSquareChat(rq)
        
    @loggedIn
    def inviteToSquare(self, squareMid, squareChatMid, invitees=[]):
        rq = InviteToSquareRequest()
        rq.squareMid = squareMid
        rq.invitees = invitees
        rq.squareChatMid = squareChatMid
        return self.square.inviteToSquare(rq)
        
    @loggedIn
    def inviteToSquareChat(self, squareChatMid, inviteeMids=[]):
        rq = InviteToSquareChatRequest()
        rq.inviteeMids = inviteeMids
        rq.squareChatMid = squareChatMid
        return self.square.inviteToSquareChat(rq)
        
    @loggedIn
    def getSquareMember(self, squareMemberMid):
        rq = GetSquareMemberRequest()
        rq.squareMemberMid = squareMemberMid
        return self.square.getSquareMember(rq)
        
    @loggedIn
    def getSquareMembers(self, mids=[]):
        rq = GetSquareMembersRequest()
        rq.mids = mids
        return self.square.getSquareMembers(rq)
        
    @loggedIn
    def getSquareMemberRelation(self, squareMid, targetSquareMemberMid):
        rq = GetSquareMemberRelationRequest()
        rq.squareMid = squareMid
        rq.targetSquareMemberMid = targetSquareMemberMid
        return self.square.getSquareMemberRelation(rq)
        
    @loggedIn
    def getSquareMemberRelations(self, state=1, continuationToken=None, limit=50):
        rq = GetSquareMemberRelationsRequest()
        rq.state = state # 1 NONE, 2 BLOCKED
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getSquareMemberRelations(rq)
        
    @loggedIn
    def getSquareChatMembers(self, squareChatMid, continuationToken=None, limit=50):
        rq = GetSquareChatMembersRequest()
        rq.squareChatMid = squareChatMid
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getSquareChatMembers(rq)
        
    @loggedIn
    def getSquareChatStatus(self, squareChatMid):
        rq = GetSquareChatStatusRequest()
        rq.squareChatMid = squareChatMid
        return self.square.getSquareChatStatus(rq)
        
    @loggedIn
    def getSquareChat(self, squareChatMid):
        rq = GetSquareChatStatusRequest()
        rq.squareChatMid = squareChatMid
        return self.square.getSquareChat(rq)
        
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
        
    @loggedIn
    def getJoinableSquareChats(self, squareMid, continuationToken=None, limit=50):
        rq = GetJoinableSquareChatsRequest()
        rq.squareMid = squareMid
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getJoinableSquareChats(rq)
        
    @loggedIn
    def getInvitationTicketUrl(self, mid):
        rq = GetInvitationTicketUrlRequest()
        rq.mid = mid
        return self.square.getInvitationTicketUrl(rq)