#!/usr/bin/env python
#
#  setup.py for spark-python-sdk
#  Started on 19/04/2017 by Antoine
#

from distutils.core import setup

setup(name="Sparkpy",
      version="1.0",
      description="Python module for consuming RESTful APIs for Cisco Spark",
      author="Bassintag",
      packages=['sparkpy'],
      install_requires=['requests'])
