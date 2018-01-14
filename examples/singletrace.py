# -*- coding: utf-8 -*-
from linepy import *

line = LINE('EMAIL', 'PASSWORD')
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))
line.log("Timeline Token : " + str(line.tl.channelAccessToken))

# Initialize OEPoll with LINE instance
oepoll = OEPoll(line)

while True:
    try:
        ops=oepoll.singleTrace(count=50)
        
        for op in ops:
            # Receive messages
            if op.type == OpType.RECEIVE_MESSAGE:
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

                try:
                    # Check content only text message
                    if msg.contentType == 0:
                        # Check only group chat
                        if msg.toType == 2:
                            # Chat checked request
                            line.sendChatChecked(receiver, msg_id)
                            # Get sender contact
                            contact = line.getContact(sender)
                            # Command list
                            if text.lower() == 'hi':
                                line.log('[%s] %s' % (contact.displayName, text))
                                line.sendMessage(receiver, 'Hi too! How are you?')
                            elif text.lower() == '/author':
                                line.log('[%s] %s' % (contact.displayName, text))
                                line.sendMessage(receiver, 'My author is linepy')
                except Exception as e:
                    line.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
            # Auto join if BOT invited to group
            elif op.type == OpType.NOTIFIED_INVITE_INTO_GROUP:
                try:
                    group_id=op.param1
                    # Accept group invitation
                    line.acceptGroupInvitation(group_id)
                except Exception as e:
                    line.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))
            else:
                pass

            # Don't remove this line, if you wan't get error soon!
            oepoll.setRevision(op.revision)
            
    except Exception as e:
        line.log("[SINGLE_TRACE] ERROR : " + str(e))