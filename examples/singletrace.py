# -*- coding: utf-8 -*-
from linepy import *

client = LineClient()
#client = LineClient(authToken='AUTHTOKEN')

client.log("Auth Token : " + str(client.authToken))

# Initialize LineChannel with LineClient
channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))

poll = LinePoll(client)

while True:
    try:
        ops=poll.singleTrace(count=50)
        
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
            elif op.type == OpType.NOTIFIED_INVITE_INTO_GROUP:
                try:
                    group_id=op.param1
                    # Accept group invitation
                    client.acceptGroupInvitation(group_id)
                except Exception as e:
                    client.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))
            else:
                pass

            # Don't remove this line, if you wan't get error soon!
            poll.setRevision(op.revision)
            
    except Exception as e:
        client.log("[SINGLE_TRACE] ERROR : " + str(e))
