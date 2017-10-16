# -*- coding: utf-8 -*-
"""
LINE Python -- LINE Messaging's private API
=========================================

    >>> from linepy import *

Links
`````

* `GitHub repository <https://github.com/fadhiilrachman/line-py>`_

"""
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   long_description = ''
   
setup(
    name='linepy',
    packages=['linepy'],
    python_requires='>=2.7',
    version='1.5',
    license='BSD License',
    author='Fadhiil Rachman',
    author_email='fadhiilrachman@gmail.com',
    url='https://github.com/fadhiilrachman/line-py',
    description=' LINE Messaging\'s private API',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Communications :: Chat',
    ],
    install_requires=[
        'akad',
        'requests',
        'rsa'
    ],
)