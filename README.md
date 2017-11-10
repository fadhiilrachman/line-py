# ![logo](/examples/assets/LINE-sm.png) LINE Python

 [![Version 1.6.5](https://img.shields.io/badge/stable-1.6.5-brightgreen.svg "Version 1.6.5")](https://pypi.python.org/pypi/linepy) [![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 2.7, 3.x](https://img.shields.io/badge/python-2.7%2C%203.x-green.svg "Supported python versions: 2.7, 3.x")](https://pypi.python.org/pypi/linepy) [![Supported python versions: 2.7, 3.x](https://img.shields.io/badge/chat-on%20discord-7289da.svg "Chat on Discord")](https://discord.gg/JAA2uk6)

*LINE Messaging's private API*

----

## Requirement

The linepy module only requires Python 2.7, or Python 3. You can download from [here](https://www.python.org/downloads/). 

## Installation

Installation is simple. It can be installed from pip using the following command:
```sh
$ pip install linepy
```
Or from the code:
```sh
$ python setup.py install
```

## Usage

```python
>>> from linepy import *
>>> client = LineClient()
>>> client.log("Auth Token : " + str(client.authToken))
```

### Examples

All examples can be found [here](https://github.com/fadhiilrachman/line-py/tree/master/examples).

## Updates

From pip using the following command:
```sh
$ pip install linepy --upgrade
```

### Change Log

**2017.11.10**

* Implement object message in forwardObjectMsg
* Implement personalization in updateProfilePicture and updateProfileCover
* Improve LineChannel and LineServer
* You can set manually showing QR Code if login with QR

**2017.11.06**

* Fix sendMessageWithMention
* Improve sendMessage make doesn't work with type dict
* Typo of setChannelHeaders statement

**2017.10.23**

* Improve multi login from instance LineClient
* QR login now showing QR ASCII from terminal with [PyQRCode](https://pypi.python.org/pypi/PyQRCode)
* Now you can send media (image, video, audio, file) with URL
* Implement LINE Timeline

**2017.10.16**

Initial release

## Author
Fadhiil Rachman / [@fadhiilrachman](https://www.instagram.com/fadhiilrachman)

### Special thanks
- [carpedm20](https://github.com/carpedm20)
- [Matti Virkkunen](http://altrepo.eu/git/line-protocol)
