# Changelog

All notable changes to this project will be documented in this file.

----

**2017.12.03**

* Fix several bugs
* Implement sendSticker, sendContact and sendGift in LineClient instance

**2017.11.24**

* Implement singleTrace() for Long polling operations
* Add new examples: BOT for group and single trace
* Implement LineTimeline() with new several function
* Implement LineObject() with merge several function from LineModels
* Now you can send GIF image with sendGIF() and sendGIFWithURL() (thanks to [Dosugamea](https://github.com/fadhiilrachman/line-py/pull/4))
* You can add optional AppName or PhoneName from instance LineClient()

**2017.11.18**

* Fix some typo in LineModels
* Fixing updateProfileCover (Still in development)

**2017.11.16**

* Implement profile personalization with updateProfileVideoPicture()
* Implement updateGroupPicture for group chat
* Improve LineChannel and LineModels
* Add LINE_SQUARE_QUERY_PATH in LineServer instance for LINE Square *soon

**2017.11.11**

* Fix some error and typo in LineModels

**2017.11.10**

* Now you can forward object message with forwardObjectMsg()
* Implement profile personalization with updateProfilePicture() and updateProfileCover()
* Improve LineChannel and LineServer

**2017.11.06**

* Fix sendMessageWithMention
* Improve sendMessage make doesn't work with type dict
* Typo of setChannelHeaders statement

**2017.10.23**

* Improve multi login from instance LineClient()
* QR login now showing QR ASCII from terminal with [PyQRCode](https://pypi.python.org/pypi/PyQRCode)
* Now you can send media (image, video, audio, file) with URL
* Implement LINE Timeline

**2017.10.16**

Initial release
