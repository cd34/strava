#!/usr/bin/env python

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

from strava import Athlete

"""
First, we set up a Strava Object for the Athlete that we want to query
We've done this through the Oauth2 tools located in the oauth_setup
directory.
"""
st = Athlete(access_token=config.get('user', 'access_token'))

"""
Once we've gotten the Athlete's object, we can then look at various
statistics - number of activities and total moving time are shown below.
By default, we only look at the last 7 days.
"""
#stats = st.activity_stats()

#print('Ridden %d activites' % stats['activities'])
#print('Total moving time: %f minutes' %
#      (float(stats['moving_time']) / 60.0))

"""
We can then iterate through the activities, and further through the segments
on each of those activities, displaying information from each. Ride details
are stored in metric, so, we need to convert that to get imperial measurements.
"""

for activity in st.activities():
    print('Ride name: %s' % activity.name)
    # convert from m/s to mph
    # m/s * 2.23694 = mph
    print('Average speed: %.1f mph' % (activity.detail['average_speed'] \
        * 2.23694))
    print('Average watts: %d' % activity.detail['average_watts'])
    for segment in activity.segments:
        print('  Segment: %s\n    Moving Time: %f minutes\n    Average '
              'Speed: %f mph' %
              (segment.name, segment.detail['moving_time'] / 60.0,
               segment.detail.average_speed * 2.23694))
