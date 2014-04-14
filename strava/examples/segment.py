#!/usr/bin/env python

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

from strava import Segment

st = Segment(access_token=config.get('user', 'access_token'), effort=610242)

"""
{u'athlete_count': 375, u'updated_at': u'2014-04-13T13:00:54Z', u'private': False, u'elevation_low': 120.9, u'end_latitude': 37.226973, u'id': 610242, u'city': u'Los Gatos', u'elevation_high': 138.7, u'start_longitude': -121.98443, u'state': u'CA', u'average_grade': 0.0, u'map': {u'resource_state': 3, u'polyline': u'mzebFtapgVlBl@dC~@f@v@Q|@c@lA_@p@eEgBaCy@i@Lc@l@Ed@s@pCw@hEy@lA_@IcA}@cD{CGsArBwDxDwHp@c@z@RjExA', u'id': u's610242'}, u'end_longitude': -121.984348, u'hazardous': False, u'start_latlng': [37.226794, -121.98443], u'end_latlng': [37.226973, -121.984348], u'starred': True, u'distance': 1441.52, u'climb_category': 0, u'name': u"Cat's Hill Crit Lap", u'total_elevation_gain': 21.16, u'country': u'United States', u'created_at': u'2010-05-02T20:26:31Z', u'maximum_grade': 17.8, u'resource_state': 3, u'effort_count': 7435, u'start_latitude': 37.226794, u'activity_type': u'Ride'}}
"""

print 'Segment:', st.detail['name']
print 'Elevations:', st.detail.elevations
print 'Distance:', st.detail['distance']
print 'Athlete Count:', st.detail['athlete_count']
print 'City, State, Country:', st.detail['city'], st.detail['state'], \
    st.detail['country']
