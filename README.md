# ![logo](/examples/assets/LINE-sm.png) LINE Python

 [![Version 3.0.8](https://img.shields.io/badge/beta-3.0.8-brightgreen.svg "Version 3.0.8")](https://pypi.python.org/pypi/linepy) [![LICENSE](https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 3.x](https://img.shields.io/badge/python-3.x-green.svg "Supported python versions: 3.x")](https://www.python.org/downloads/) [![Chat on Discord](https://discordapp.com/api/guilds/370888828489170956/widget.png "Chat on Discord")](https://discord.gg/JAA2uk6)

*LINE Messaging's private API*

----

## Requirement

The linepy module only requires Python 3. You can download from [here](https://www.python.org/downloads/). 

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
>>> line = LINE('EMAIL', 'PASSWORD')
>>> line.log("Auth Token : " + str(line.authToken))
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
