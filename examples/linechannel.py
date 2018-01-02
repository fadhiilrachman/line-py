# -*- coding: utf-8 -*-
from linepy import *

client = LineClient()
#client = LineClient(authToken='AUTHTOKEN')

client.log("Auth Token : " + str(client.authToken))

# Initialize LineChannel with LineClient
channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))
