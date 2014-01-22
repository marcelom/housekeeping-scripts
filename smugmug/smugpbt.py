#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import json

#API_KEY='E3VwzE0hgcpRMaUWG4taQanT8I9qPlpr'
API_KEY='VQbsN2RNqtvowK7wxtmqbJIMQEvhQmq9'
USER_AGENT='PersonalBackupTool/1.0'

import getpass
#email = raw_input("Enter your email: ")
password = getpass.getpass("Enter your password:")

url = 'https://api.smugmug.com/services/api/json/1.2.2/'
params = {'APIKey' : API_KEY,
          'EmailAddress' : 'marcelosm@gmail.com',
          'Password' : password,
          'method' : 'smugmug.login.withPassword' }
headers = { 'User-Agent' : USER_AGENT }

data = urllib.urlencode(params)
data = data.encode('utf-8')
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page

sessionid = json.loads(the_page)['Login']['Session']['id']

print 'login successful: %s' % sessionid

params = {'method' : 'smugmug.albums.get',
          #'APIKey' : API_KEY,
          'SessionID' : sessionid }

data = urllib.urlencode(params)
data = data.encode('utf-8')
print data
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()

print the_page
