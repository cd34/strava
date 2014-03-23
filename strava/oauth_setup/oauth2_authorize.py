#!/usr/bin/env python

"""
This is a quick stub app to generate a URL that allows you to authorize
an app from the command line. It will redirect to localhost (which may
or may not resolve) and you need to pull the &code= value out to save
that for your app.
"""

import ConfigParser
import os

from requests_oauthlib import OAuth2Session

url = 'https://www.strava.com/oauth/authorize'

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

strava = OAuth2Session(config.get('strava', 'client_id'),
             redirect_uri=config.get('strava', 'redirect_uri'))
authorization_url, state = strava.authorization_url(url)

print 'Please go to %s and authorize access.' % authorization_url
