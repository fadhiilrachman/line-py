# -*- coding: utf-8 -*-
from linepy import *

client = LineClient()
#client = LineClient(authToken='AUTHTOKEN')

client.log("Auth Token : " + str(client.authToken))

# Initialize LineChannel with LineClient
# This channel id is Timeline channel
channel = LineChannel(client, channelId="1341209950")
client.log("Channel Access Token : " + str(channel.channelAccessToken))
