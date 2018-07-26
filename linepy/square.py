# -*- coding: utf-8 -*-
from akad.ttypes import *
from random import randint

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isSupportSquare:
            if args[0].isLogin:
                return func(*args, **kwargs)
            else:
                args[0].callback.other('You want to call the function, you must login to LINE')
        else:
            args[0].callback.other('Your LINE account doesn\'t support Square')
    return checkLogin

class Square(object):
    isSupportSquare = False
    isLogin = False

    def __init__(self):
        self.isLogin = True
        try:
            self.isSupportSquare = True
            self.squares    = self.getJoinedSquares().squares
            self.squareObsToken = self.acquireEncryptedAccessToken(2).split('\x1e')[1]
        except:
            self.isSupportSquare = False
            self.log('Your LINE account doesn\'t support Square')

    """Object"""

    @loggedIn
    def sendSquareImage(self, squareChatMid, path): # Under development
        return self.uploadObjSquare(squareChatMid=squareChatMid, path=path, type='image', returnAs='bool')

    @loggedIn
    def sendSquareImageWithURL(self, squareChatMid, url): # Under development
        path = self.downloadFileURL(url, 'path')
        return self.sendSquareImage(squareChatMid, path)

    @loggedIn
    def sendSquareGIF(self, squareChatMid, path): # Under development
        return self.uploadObjSquare(squareChatMid=squareChatMid, path=path, type='gif', returnAs='bool')

    @loggedIn
    def sendSquareGIFWithURL(self, squareChatMid, url): # Under development
        path = self.downloadFileURL(url, 'path')
        return self.sendSquareGIF(squareChatMid, path)

    @loggedIn
    def sendSquareVideo(self, squareChatMid, path): # Under development
        return self.uploadObjSquare(squareChatMid=squareChatMid, path=path, type='video', returnAs='bool')

    @loggedIn
    def sendSquareVideoWithURL(self, squareChatMid, url): # Under development
        path = self.downloadFileURL(url, 'path')
        return self.sendSquareVideo(squareChatMid, path)

    @loggedIn
    def sendSquareAudio(self, squareChatMid, path): # Under development
        return self.uploadObjSquare(squareChatMid=squareChatMid, path=path, type='audio', returnAs='bool')

    @loggedIn
    def sendSquareAudioWithURL(self, squareChatMid, url): # Under development
        path = self.downloadFileURL(url, 'path')
        return self.sendSquareAudio(squareChatMid, path)

    @loggedIn
    def sendSquareFile(self, squareChatMid, path): # Under development
        return self.uploadObjSquare(squareChatMid=squareChatMid, path=path, type='file', returnAs='bool')

    @loggedIn
    def sendSquareFileWithURL(self, squareChatMid, url, fileName=''): # Under development
        path = self.downloadFileURL(url, 'path')
        return self.sendSquareFile(squareChatMid, path, fileName)

    """Square Message"""
        
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
        if squareChatMid not in self._messageReq:
            self._messageReq[squareChatMid] = -1
        self._messageReq[squareChatMid] += 1
        rq.squareMessage.squareMessageRevision = self._messageReq[squareChatMid]
        return self.square.sendMessage(rq)

    @loggedIn
    def sendSquareSticker(self, squareChatMid, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendSquareMessage(squareChatMid, '', contentMetadata, 7)
        
    @loggedIn
    def sendSquareContact(self, squareChatMid, mid):
        contentMetadata = {'mid': mid}
        return self.sendSquareMessage(squareChatMid, '', contentMetadata, 13)

    @loggedIn
    def sendSquareGift(self, squareChatMid, productId, productType):
        if productType not in ['theme','sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 10)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendSquareMessage(squareChatMid, '', contentMetadata, 9)
        
    @loggedIn
    def destroySquareMessage(self, squareChatMid, messageId):
        rq = DestroyMessageRequest()
        rq.squareChatMid = squareChatMid
        rq.messageId = messageId
        return self.square.destroyMessage(rq)

    """Square"""
        
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
    def deleteSquare(self, mid):
        rq = DeleteSquareRequest()
        rq.mid = mid
        rq.revision = self.revision
        return self.square.deleteSquare(rq)

    @loggedIn
    def deleteSquareChat(self, squareChatMid):
        rq = DeleteSquareChatRequest()
        rq.squareChatMid = squareChatMid
        rq.revision = self.revision
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
        rq.reqSeq = self.revision
        rq.squareChat = SquareChat()
        rq.squareChat.squareMid = squareMid
        rq.squareChat.name = name
        rq.squareMemberMids = squareMemberMids
        return self.square.createSquareChat(request)
        
    @loggedIn
    def fetchSquareChatEvents(self, squareChatMid, subscriptionId=0, syncToken='', limit=50, direction=2):
        rq = FetchSquareChatEventsRequest()
        rq.squareChatMid = squareChatMid
        rq.subscriptionId = subscriptionId
        rq.syncToken = syncToken
        rq.limit = limit
        rq.direction = direction
        return self.square.fetchSquareChatEvents(rq)
        
    @loggedIn
    def fetchMyEvents(self, subscriptionId=0, syncToken='', continuationToken=None, limit=50):
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
    def leaveSquareChat(self, squareChatMid, squareChatMemberRevision, sayGoodbye=True):
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
        return self.square.joinSquare(rq)
        
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
        rq = GetSquareChatRequest()
        rq.squareChatMid = squareChatMid
        return self.square.getSquareChat(rq)
        
    @loggedIn
    def getSquare(self, mid):
        rq = GetSquareRequest()
        rq.mid = mid
        return self.square.getSquare(rq)
        
    @loggedIn
    def getSquareChatAnnouncements(self, squareChatMid):
        rq = GetSquareChatAnnouncementsRequest()
        rq.squareChatMid = squareChatMid
        return self.square.getSquareChatAnnouncements(rq)
        
    @loggedIn
    def deleteSquareChatAnnouncement(self, squareChatMid, announcementSeq):
        rq = DeleteSquareChatAnnouncementRequest()
        rq.squareChatMid = squareChatMid
        rq.squareChatMid = announcementSeq
        return self.square.deleteSquareChatAnnouncement(rq)
        
    @loggedIn
    def createSquareChatAnnouncement(self, squareChatMid, text, messageId='', senderSquareMemberMid=''):
        rq = CreateSquareChatAnnouncementRequest()
        rq.reqSeq = 0
        rq.squareChatMid = squareChatMid
        rq.squareChatAnnouncement = SquareChatAnnouncement()
        rq.squareChatAnnouncement.announcementSeq = 0
        rq.squareChatAnnouncement.type = 0
        rq.squareChatAnnouncement.contents = SquareChatAnnouncementContents()
        rq.squareChatAnnouncement.contents.textMessageAnnouncementContents = TextMessageAnnouncementContents()
        rq.squareChatAnnouncement.contents.textMessageAnnouncementContents.messageId = messageId
        rq.squareChatAnnouncement.contents.textMessageAnnouncementContents.text = text
        rq.squareChatAnnouncement.contents.textMessageAnnouncementContents.senderSquareMemberMid = senderSquareMemberMid
        return self.square.createSquareChatAnnouncement(rq)

    @loggedIn
    def getJoinedSquares(self, continuationToken=None, limit=50):
        rq = GetJoinedSquaresRequest()
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getJoinedSquares(rq)

    @loggedIn
    def getJoinedSquareChats(self, continuationToken=None, limit=50):
        rq = GetJoinedSquareChatsRequest()
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.getJoinedSquareChats(rq)
        
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
        
    @loggedIn
    def getSquareStatus(self, squareMid):
        rq = GetSquareStatusRequest()
        rq.squareMid = squareMid
        return self.square.getSquareStatus(rq)
        
    @loggedIn
    def getNoteStatus(self, squareMid):
        rq = GetNoteStatusRequest()
        rq.squareMid = squareMid
        return self.square.getNoteStatus(rq)
        
    @loggedIn
    def searchSquares(self, query, continuationToken=None, limit=50):
        rq = SearchSquaresRequest()
        rq.query = query
        rq.continuationToken = continuationToken
        rq.limit = limit
        return self.square.searchSquares(rq)
        
    @loggedIn
    def refreshSubscriptions(self, subscriptions=[]):
        rq = RefreshSubscriptionsRequest()
        rq.subscriptions = subscriptions
        return self.square.refreshSubscriptions(rq)
        
    @loggedIn
    def removeSubscriptions(self, unsubscriptions=[]):
        rq = RemoveSubscriptionsRequest()
        rq.unsubscriptions = unsubscriptions
        return self.square.removeSubscriptions(rq)
