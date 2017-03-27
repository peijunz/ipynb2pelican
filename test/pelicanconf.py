#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pyembed.rst import PyEmbedRst
PyEmbedRst().register()

AUTHOR = 'Peijun Zhu'
SITENAME = "Peijun's Thoughts"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('Contact Me', 'mailto:pez33@pitt.edu'),)

# Social widget
SOCIAL = (('github', 'http://github.com/peijunz'),
          ('facebook', 'https://www.facebook.com/people/Peijun-Zhu/100011384055583'),)

DEFAULT_PAGINATION = 6
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
MARKUP = ('md', 'ipynb')
PLUGIN_PATH = ['../../']
PLUGINS = ['ipynb2pelican']

IGNORE_FILES = ['.ipynb_checkpoints']
