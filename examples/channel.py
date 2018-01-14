# -*- coding: utf-8 -*-
from linepy import *

line = LINE()
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))

# Initialize Channel with LINE
channel = Channel(line, line.server.CHANNEL_ID['LINE_MUSIC'])
channelToken = channel.getChannelResult()
line.log("Channel Token : " + str(channelToken))