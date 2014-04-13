#!/usr/bin/env python

"""
This is a quick stub app to generate a URL that allows you to authorize
an app from the command line. It will redirect to localhost (which may
or may not resolve) and you need to pull the &code= value out to save
that for your app.
"""



import ConfigParser
import os
import sys

import requests

url = 'https://www.strava.com/oauth/token'

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

if len(sys.argv) == 2:
    params = {'client_id':config.get('strava', 'client_id'),
              'client_secret':config.get('strava', 'client_secret'),
              'code':sys.argv[1],
    }
    r = requests.post(url, params=params)
    print 'access_token = {token}'.format(token=r.json()['access_token'])
else:
    print """
You must specify a code, i.e. {script} 1234
""".format(script=sys.argv[0])

