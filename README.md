# LINE Python

*LINE Messaging's private API*

----

### Installation

```sh
$ pip install linepy
```
- **Requires:** [Python 3.x](https://www.python.org/downloads/) (Works with Python 2.x, but i can't recommend)

### Update

```sh
$ pip install linepy --upgrade
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
