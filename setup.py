#!/usr/bin/env python
#
#  setup.py for spark-python-sdk
#  Started on 19/04/2017 by Antoine
#

from distutils.core import setup

setup(name="Sparkpy",
      version="1.1",
      description="Python module for consuming RESTful APIs for Cisco Spark",
      author="Bassintag",
      url="https://github.com/Bassintag551/spark-python-sdk",
      packages=['sparkpy'],
      install_requires=['requests'],
      classifiers=["Programming Language :: Python :: 3"])
