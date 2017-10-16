# -*- coding: utf-8 -*-
from linepy import *

client = LineClient()
#client = LineClient(authToken='AUTHTOKEN')

client.log("Auth Token : " + str(client.authToken))

poll = LinePoll(client)

# Receive messages from LinePoll
def RECEIVE_MESSAGE(op):
    msg = op.message

    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from

    if msg.contentType == 0:
        contact = client.getContact(receiver)
        txt = '[%s] %s' % (contact.displayName, text)
        client.sendMessage(receiver, txt)
        client.log(txt)

# Add function to LinePoll
poll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})

while True:
    poll.trace()