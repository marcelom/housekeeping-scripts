#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import urllib
import urllib2
import json
import cookielib
import getpass
import sys
import threading
import Queue
import hashlib

API_KEY      = 'VQbsN2RNqtvowK7wxtmqbJIMQEvhQmq9'
USER_AGENT   = 'PersonalBackupTool/1.0'
API_ENDPOINT = 'https://api.smugmug.com/services/api/json/1.2.2/'
HEADERS      = { 'User-Agent': 'PersonalBackupTool/1.0' }

cj           = cookielib.CookieJar()
urlopener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

q = Queue.Queue()

def smugopen(params={}):
    data = urllib.urlencode(params).encode('utf-8')
    req = urllib2.Request(API_ENDPOINT, data, HEADERS)
    return json.loads(urlopener.open(req).read())

def error(s):
    print "Unable to execute method '%s', with reason '%s' (code %s)" % (s['method'], s['message'], s['code'])
    sys.exit(1)

def downloader():
    while True:
        item = q.get() # albumpath, image
        fname = item[0] + "/" + item[1]['FileName']
        if os.path.isfile(fname):
            f = open(fname)
            if hashlib.md5(f.read()).hexdigest() == item[1]['MD5Sum']:
                print "Found file '%s': Skipping because MD5 matches." % fname
                f.close()
                q.task_done()
                continue
        f = open(fname, "wb")
        req = urllib2.Request(item[1]['OriginalURL'], "", HEADERS)
        f.write(urlopener.open(req).read())
        f.close()
        print "Found file '%s': Downloaded OK." % fname
        q.task_done()

email = raw_input("Enter your email: ")
#email = 'marcelosm@gmail.com'
password = getpass.getpass("Enter your password:")

params = dict(APIKey=API_KEY, EmailAddress=email, Password=password, method='smugmug.login.withPassword')
login = smugopen(params)

if login['stat']=='ok':
    z = login['Login']
    print "Logged in successfully. Account Status: '%s', Account Type: '%s', Session ID: '%s'" % (z['AccountStatus'],z['AccountType'],z['Session']['id'])
else:
    error(login)

params = dict(method='smugmug.albums.get')
albums = smugopen(params)

if albums['stat']=='ok':
    print "Successfully retrieved list of albums."
else:
    error(albums)

t = threading.Thread(target=downloader)
t.daemon = True
t.start()

for a in albums['Albums']:
    id = a['id']
    key = a['Key']
    title = a['Title']
    cat = a['Category']['Name']
    try:
        subcat = a['SubCategory']['Name']
    except:
        subcat = ""
    print "Found album '%s/%s/%s' " % (cat,subcat,title)
    path = "./smugpbt/%s/%s" % (cat, subcat)
    if subcat!="": path += "/"
    path += title
    if not os.path.exists(path): os.makedirs(path)
    params = dict(method='smugmug.images.get', AlbumID=id, AlbumKey=key, Extras="FileName,OriginalURL,MD5Sum")
    images = smugopen(params)
    if images['stat']=='ok':
        for image in images['Album']['Images']:
            q.put( (path,image) )
    else:
        error(images)

params = dict(method='smugmug.logout')
the_page = smugopen(params)
print the_page

q.join()
