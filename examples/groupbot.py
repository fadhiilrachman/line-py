# -*- coding: utf-8 -*-
from linepy import *

client = LINE('EMAIL', 'PASSWORD')
#client = LINE('AUTHTOKEN')
#client = LINE() Qr login
client.log("Auth Token : " + str(client.authToken))
client.log("Timeline Token : " + str(client.tl.channelAccessToken))

# Initialize OEPoll with LINE instance
tracer = OEPoll(client)

# Receive messages from OEPoll
def RECEIVE_MESSAGE(op):
    '''
        This is sample for implement BOT in LINE group
        Invite your BOT to group, then BOT will auto accept your invitation
        Command availabe :
        > hi
        > /author
    '''
    msg = op.message
    
    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    
    #fix for pm case
    if msg.toType == 0: #private message
        msg.to = msg._from
    
    try:
        # Check content only text message
        if msg.contentType == 0:
            # Check only group chat
            if msg.toType == 2:
                # Chat checked request
                client.sendChatChecked(receiver, msg_id)
                # Get sender contact
                contact = client.getContact(sender)
                # Command list
                if text.lower() == 'hi':
                    client.log('[%s] %s' % (contact.displayName, text))
                    client.sendMessage(receiver, 'Hi too! How are you?')
                elif text.lower() == '/author':
                    client.log('[%s] %s' % (contact.displayName, text))
                    client.sendMessage(receiver, 'My author is linepy')
    except Exception as e:
        client.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
    
# Auto join if BOT invited to group
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        group_id=op.param1
        #op.param2 is who invited, and op.param3 is who got invited (this might not be just you, it could  be string or list)
        # Accept group invitation
        client.acceptGroupInvitation(group_id)
    except Exception as e:
        client.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))

# Add function to OEPoll
tracer.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

while True:
    tracer.trace()
