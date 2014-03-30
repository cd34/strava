#!/usr/bin/env python

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

from strava import Segment

st = Segment(access_token=config.get('user', 'access_token'), effort=610242)

print st.detail.__dict__
