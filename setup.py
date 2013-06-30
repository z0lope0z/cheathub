#!/usr/bin/env python

from distutils.core import setup

setup(name='CheatHub',
      version='0.1',
      description='Makes you look like you are active in github',
      author='Lope Emano',
      author_email='lopeemano@gmail.com',
      url='https://github.com/z0lope0z/',
      install_requires=[
          "beautifulsoup4",
          "caldav == 0.1.4",
      ],
     )


