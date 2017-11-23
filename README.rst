.. contents::

LINE Messaging's private API

**Homepage**: https://github.com/fadhiilrachman/line-py

Requirements
============
The linepy module only requires Python 2.7, or Python 3

Installation
============
Installation is simple. It can be installed from pip using the following
command::

    $ pip install linepy

Or from the terminal::

    $ python setup.py install

Usage
============
::

    >>> from linepy import *
    >>> client = LineClient()
    >>> client.log("Auth Token : " + str(client.authToken))

All examples can be found `here <https://github.com/fadhiilrachman/line-py/tree/master/examples>`_.