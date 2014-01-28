#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import json
import cookielib
import getpass

#API_KEY='E3VwzE0hgcpRMaUWG4taQanT8I9qPlpr'
API_KEY='VQbsN2RNqtvowK7wxtmqbJIMQEvhQmq9'
USER_AGENT='PersonalBackupTool/1.0'

#email = raw_input("Enter your email: ")
password = getpass.getpass("Enter your password:")

url = 'https://api.smugmug.com/services/api/json/1.2.2/'
params = {'APIKey' : API_KEY,
          'EmailAddress' : 'marcelosm@gmail.com',
          'Password' : password,
          'method' : 'smugmug.login.withPassword' }
headers = { 'User-Agent' : USER_AGENT }

# Setup a few important helpers...
# cj is our cookie jar, urlopener is our cookie enabled urllib2 opener.
cj = cookielib.CookieJar()
urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

data = urllib.urlencode(params)
data = data.encode('utf-8')
req = urllib2.Request(url, data, headers)
response = urlopener.open(req)
the_page = response.read()

print the_page
print cj

#sessionid = json.loads(the_page)['Login']['Session']['id']

#print 'login successful: %s' % sessionid

params = {'method' : 'smugmug.albums.get' }
          #'APIKey' : API_KEY,
          #'SessionID' : sessionid }

data = urllib.urlencode(params)
data = data.encode('utf-8')
print data
req = urllib2.Request(url, data, headers)
response = urlopener.open(req)
the_page = response.read()

print the_page
