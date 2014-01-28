#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import json
import cookielib
import getpass

API_KEY      = 'VQbsN2RNqtvowK7wxtmqbJIMQEvhQmq9'
USER_AGENT   = 'PersonalBackupTool/1.0'
API_ENDPOINT = 'https://api.smugmug.com/services/api/json/1.2.2/'
HEADERS      = { 'User-Agent' : USER_AGENT }

cj           = cookielib.CookieJar()
urlopener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def smugopen(params={}):
	data = urllib.urlencode(params)
	data = data.encode('utf-8')
	req = urllib2.Request(API_ENDPOINT, data, HEADERS)
	response = urlopener.open(req)
	the_page = response.read()
	return the_page

#email = raw_input("Enter your email: ")
password = getpass.getpass("Enter your password:")

params = {'APIKey' : API_KEY,
          'EmailAddress' : 'marcelosm@gmail.com',
          'Password' : password,
          'method' : 'smugmug.login.withPassword' }
the_page = smugopen(params)
print the_page

params = {'method' : 'smugmug.albums.get' }
the_page = smugopen(params)
print the_page

params = {'method' : 'smugmug.logout' }
the_page = smugopen(params)
print the_page