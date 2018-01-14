# -*- coding: utf-8 -*-
from linepy import *

line = LINE('EMAIL', 'PASSWORD')
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))

# Initialize OEPoll with LINE instance
oepoll = OEPoll(line)

# Receive messages from OEPoll
def RECEIVE_MESSAGE(op):
    msg = op.message

    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    
    # Check content only text message
    if msg.contentType == 0:
        # Check only group chat
        if msg.toType == 2:
            # Get sender contact
            contact = line.getContact(sender)
            txt = '[%s] %s' % (contact.displayName, text)
            # Send a message
            line.sendMessage(receiver, txt)
            # Print log
            line.log(txt)

# Add function to OEPoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})

while True:
    oepoll.trace()
