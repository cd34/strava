#!/usr/bin/env python

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

from strava import Athlete

st = Athlete(access_token=config.get('user', 'access_token'))

#print st.athlete

print('Ridden %d rides' % st.activity_stats()['rides'])
print('Total moving time: %f minutes' %
      (float(st.ride_stats()['moving_time']) / 60.0))
