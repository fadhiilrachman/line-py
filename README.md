# ![logo](/examples/assets/LINE-sm.png) LINE Python

 [![Version 1.5](https://img.shields.io/badge/stable-1.5-brightgreen.svg "Version 1.5")](https://pypi.python.org/pypi/linepy/1.5) [![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 2.7, 3.x](https://img.shields.io/badge/python-2.7%2C%203.x-green.svg "Supported python versions: 2.7, 3.x")](https://pypi.python.org/pypi/linepy)

*LINE Messaging's private API*

----

### Installation

Python 2.7 :
```sh
$ pip install linepy
```
Python 3.x :
```sh
$ pip3 install linepy
```
- **Requires:** [Python 3.x](https://www.python.org/downloads/) (Works with Python 2.x, but i can't recommend)

### Updating

Python 2.7 :
```sh
$ pip install linepy --upgrade
```
Python 3.x :
```sh
$ pip3 install linepy --upgrade
```

### Special thanks
- [carpedm20](https://github.com/carpedm20)
- [Matti Virkkunen](http://altrepo.eu/git/line-protocol)

Update
------

**2017.10.16**

Initial release

## How to use

```python
from linepy import *
client = LineClient()
client.log("Auth Token : " + str(client.authToken))
```

### Examples

All examples can be found [here](https://github.com/fadhiilrachman/line-py/tree/master/examples).
