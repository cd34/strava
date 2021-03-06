#!/usr/bin/env python

"""Wrapper for the Strava (http://www.strava.com) API.

See https://stravasite-main.pbworks.com/w/browse/ for API documentation."""

__author__    = "Brian Landers"
__contact__   = "brian@packetslave.com"
__copyright__ = "Copyright 2012, Brian Landers"
__license__   = "Apache"
__version__   = "1.0"


BASE_API = 'https://www.strava.com/api/v3'

from collections import defaultdict
from datetime import date, timedelta
import json
from types import IntType

try:
    import urllib2
except ImportError:
    import urllib
    urllib2 = False
from urllib import urlencode


class APIError(Exception):
    pass


class StravaObject(object):
    """Base class for interacting with the Strava API endpoint."""
    access_token = None
 
    def __init__(self, **kwargs):
        if kwargs.get('access_token'):
            self.access_token = kwargs.get('access_token')

    #noinspection PyUnresolvedReferences
    def load(self, url, key=None, params=None):
        if params:
            url = '{url}?{params}'.format(url=url,
                params=urlencode(params, True))
        headers = {'Authorization':
            'Bearer {access_token}'.format(access_token=self.access_token)}
        if urllib2:
            try:
                req = urllib2.Request(BASE_API + url,
                    headers=headers)
                rsp = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                raise APIError('%s: request failed: %s' % (url, e))
        else:
            try:
                rsp = urllib.request.urlopen(BASE_API + url,
                    headers=headers)
            except urllib.error.HTTPError as e:
                raise APIError('%s: request failed: %s' % (url, e))
        txt = rsp.read().decode('utf-8')

        try:
            return json.loads(txt)
        except (ValueError, KeyError) as e:
            raise APIError('%s: parsing response failed: %s' % (url, e))

    @property
    def id(self):
        # TODO figure out why some activities fail here
        try:
            return self._id
        except:
            print self.__dict__


class Athlete(StravaObject):
    """Encapsulates data about a single Athlete.

    Note that the athlete's name is NOT available through this API. You have to
    load a activity or effort to get that data from the service, and we don't
    want to make that heavy a query at the top level.
    """
    def __init__(self, **kwargs):
        super(Athlete, self).__init__(**kwargs)
        if kwargs.get('access_token'):
            self.access_token = kwargs.get('access_token')
        self._url = '/athlete'

    def athlete(self, id=None):
        # allowed to look at other athletes, cannot list other
        # athlete activities
        url = self._url
        if id:
            self._url = '/athletes'
            url = '/'.join([self._url, str(id)])
        return self.load(url)

    def activities(self, **kwargs):
        self._url = '/activities'
        params = {}
        if 'page' in kwargs:
            params['page'] = kwargs.pop('page')
        if 'per_page' in kwargs:
            params['per_page'] = kwargs.pop('per_page')
        if 'before' in kwargs:
            params['before'] = kwargs.pop('before')
        if 'after' in kwargs:
            params['after'] = kwargs.pop('after')
        if 'following' in kwargs:
            self._url += '/following'

        out = []

        for activity in self.load(self._url, params=params):
            out.append(Activity(id=activity['id'], name=activity['name'],
                access_token=self.access_token))

        return out

    def activity_stats(self, days=7):
        """Get number of activities, time, and distance for the past N days."""
        start = date.today() - timedelta(days=days)
        stats = defaultdict(float)
        
        for activity in self.activities(start_date=start):
            stats['activities'] += 1
            stats['moving_time'] += activity.detail.moving_time
            stats['distance'] += activity.detail.distance

        return stats

    def friends(self):
        """
GET https://www.strava.com/api/v3/athlete/friends
GET https://www.strava.com/api/v3/athletes/:id/friends
        """
        pass
    
    def followers(self):
        """
GET https://www.strava.com/api/v3/athlete/followers
GET https://www.strava.com/api/v3/athletes/:id/followers
        """
        pass
    
    def both_following(self):
        """
GET https://www.strava.com/api/v3/athletes/:id/both-following
        """
        pass
    
    def kom_qom_crs(self):
        """
GET https://www.strava.com/api/v3/athletes/:id/koms
        """
        pass
    
        
class Activity(StravaObject):
    """Information about a single activity.

    Most of the activity data is encapsulated in a ActivityDetail instance,
    accessible via the "detail" property. This lets us lazy-load the details,
    and saves an API round-trip if all we care about is the ID or name of
    the activity.
    """
    def __init__(self, **kwargs):
        super(Activity, self).__init__(**kwargs)
        self._id = kwargs['id']
        self._name = kwargs.get('name', '')
        self._detail = None
        self._segments = []
        
    @property
    def name(self):
        return self._name

    @property
    def detail(self):
        if not self._detail:
            self._detail = ActivityDetail(id=self.id,
                access_token=self.access_token)
        return self._detail

    @property
    def segments(self):
        if not self._segments:
            for effort in self._detail['segment_efforts']:
                self._segments.append(Segment(effort=effort, \
                access_token=self.access_token))
        return self._segments


class ActivityDetail(StravaObject):
    
    def __init__(self, **kwargs):
        super(ActivityDetail, self).__init__(**kwargs)
        self._attr = self.load('/activities/%s' % kwargs['id'], 'activity')

    def __getitem__(self, key):
        try:
            return self._attr[key]
        except KeyError:
            raise APIError('Invalid key: {key}'.format(key=key))


class Segment(StravaObject):
    """Information about a single activity segment.

    Most of the data is encapsulated in a SegmentDetail instance, accessible via
    the "detail" property. This lets us lazy-load the details, and saves an API
    round-trip if all we care about is the ID or name of the segment.

    Note that this class combines the "effort" and "segment" as Strava defines
    them. They both ultimately pertain to a given portion of a activity, so it
    makes sense to access them both through the same interface.

    This does have the side effect, however, of requiring two API round-trips to
    load the "detail" property.  It's lazy-loaded, so if you just care about the
    segment name or ID, you won't take the it.
    """
    def __init__(self, **kwargs):
        super(Segment, self).__init__(**kwargs)
        if kwargs.get('access_token'):
            self.access_token = kwargs.get('access_token')
        self._effort = kwargs['effort']
        self._detail = None

        
    @property
    def time(self):
        return self._effort['start_date_local']
    
    @property
    def name(self):
        return self._effort['name']

    @property
    def detail(self):
        if not self._detail:
            self._detail = SegmentDetail(effort=self._effort, \
            access_token=self.access_token)
        return self._detail


class SegmentDetail(StravaObject):
    def __init__(self, **kwargs):
        super(SegmentDetail, self).__init__(**kwargs)
        self._effort = kwargs['effort']
        if type(kwargs['effort']) == IntType:
            id = self._effort
            self._attr = self.load('/segments/%s' % id, 'segment')
        else:
            id = self._effort['id']
            self._attr = self.load('/segment_efforts/%s' % id, 'segment')

    def __getitem__(self, key):
        try:
            return self._attr[key]
        except KeyError:
            raise APIError('Invalid key: {key}'.format(key=key))

    @property
    def elevations(self):
        return (self._attr['elevation_low'],
                self._attr['elevation_high'],
                self._attr['total_elevation_gain'])

    @property
    def average_speed(self):
        return self._effort['segment']['distance'] / \
            self._effort['elapsed_time'] 
