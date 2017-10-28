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
    #For 1 to 1 Talk
    if msg.toType == 0:
        receiver = sender
    #Execute Message as Python script
    if msg.text[:len("!exec")] == "!exec":
        try:
            sys.stdout = open("temp.txt","w")
            exec(msg.text.replace("!exec",""))
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            with open("temp.txt","r") as r:
                txt = r.read()
                cl.sendMessage(receiver,txt)
        except Exception as e:
            txt = str(e)
            cl.sendMessage(receiver,txt)

# Add function to LinePoll
poll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})

while True:
    poll.trace()
