#!/usr/bin/env python

"""
This prints a time delta list of the segments as ridden (with a small 
correction factor) so that you can display a list of the segments
on youtube to correspond to a video
"""

import ConfigParser
import datetime
import os
import sys

from strava import Activity

def display_activity(id, time_correction=5):

    """
    First, we set up a Strava Object for the Activity that we want to query
    We've done this through the Oauth2 tools located in the oauth_setup
    directory.
    """
    activity = Activity(access_token=config.get('user', 'access_token'), \
        id=id)

    """
    We can then iterate through the activity, and further through the segments,
    displaying information from each. Ride details are stored in metric, so,
    we need to convert that to get imperial measurements.
    """

    print('Ride name: {name}'.format(name=activity.detail['name']))
    print('Strava URL: http://www.strava.com/activities/{id}' \
        .format(id=activity.detail['id']))
    print('')
    activity_start_time = datetime.datetime.strptime( \
        activity.detail['start_date_local'],'%Y-%m-%dT%H:%M:%SZ')

    for segment in activity.detail['segment_efforts']:
        segment_start_time = datetime.datetime.strptime( \
            segment['start_date_local'],'%Y-%m-%dT%H:%M:%SZ')
        segment_delta = str(segment_start_time - activity_start_time - \
            datetime.timedelta(seconds=5))
        print('{time} - {segment}'.format(time=segment_delta,
            segment=segment['name']))

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.join(os.path.abspath(__file__))))),
            'strava.cfg')))

    if len(sys.argv) == 2:
        try:
            display_activity(sys.argv[1])
        except KeyboardInterrupt:
            sys.exit()
    else:
        print """\

Usage: {0} activity_id""".format(sys.argv[0])
