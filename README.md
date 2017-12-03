# ![logo](/examples/assets/LINE-sm.png) LINE Python

 [![Version 1.8.4](https://img.shields.io/badge/stable-1.8.4-brightgreen.svg "Version 1.8.4")](https://pypi.python.org/pypi/linepy) [![LICENSE](https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 2.7, 3.x](https://img.shields.io/badge/python-2.7%2C%203.x-green.svg "Supported python versions: 2.7, 3.x")](https://pypi.python.org/pypi/linepy) [![Supported python versions: 2.7, 3.x](https://img.shields.io/badge/chat-on%20discord-7289da.svg "Chat on Discord")](https://discord.gg/JAA2uk6)

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

## Author
Fadhiil Rachman / [@fadhiilrachman](https://www.instagram.com/fadhiilrachman)

### Special thanks
- [carpedm20](https://github.com/carpedm20)
- [Matti Virkkunen](https://github.com/mvirkkunen)