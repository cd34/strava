#!/usr/bin/env python

"""Wrapper for the Strava (http://www.strava.com) API.

See https://stravasite-main.pbworks.com/w/browse/ for API documentation."""

__author__    = "Brian Landers"
__contact__   = "brian@packetslave.com"
__copyright__ = "Copyright 2012, Brian Landers"
__license__   = "Apache"
__version__   = "1.0"


BASE_API = "http://www.strava.com/api/v3"

from collections import defaultdict
from datetime import date, timedelta
import json

try:
    import urllib2
except ImportError:
    import urllib
    urllib2 = False


class APIError(Exception):
    pass


class StravaObject(object):
    """Base class for interacting with the Strava API endpoint."""
    access_token = None
 
    def __init__(self, **kwargs):
        if kwargs.get('access_token'):
            self.access_token = kwargs.get('access_token')

    #noinspection PyUnresolvedReferences
    def load(self, url, key=None):
        headers = {'Authorization':
            'Bearer {access_token}'.format(access_token=self.access_token)}
        if urllib2:
            try:
                req = urllib2.Request(BASE_API + url,
                    headers=headers)
                rsp = urllib2.urlopen(req)
            except urllib2.HTTPError as e:
                raise APIError("%s: request failed: %s" % (url, e))
        else:
            try:
                rsp = urllib.request.urlopen(BASE_API + url,
                    headers=headers)
            except urllib.error.HTTPError as e:
                raise APIError("%s: request failed: %s" % (url, e))
        txt = rsp.read().decode('utf-8')

        try:
            #if key:
            #    return json.loads(txt)[key]
            #else:
            return json.loads(txt)
        except (ValueError, KeyError) as e:
            raise APIError("%s: parsing response failed: %s" % (url, e))

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
    load a activity or effort to get that data from the service, and we don't want
    to make that heavy a query at the top level.
    """
    def __init__(self, **kwargs):
        super(Athlete, self).__init__(**kwargs)
        if kwargs.get('access_token'):
            self.access_token = kwargs.get('access_token')
        self._url = '/athlete'

    @property
    def athlete(self, id=None):
        # allowed to look at other athletes, cannot list other
        # athlete activities
        url = self._url
        if id:
            url = '/'.join(self._url, id)
        return self.load(url)

    def activities(self, start_date=None, offset=None):
        # before, after, page, per_page
        out = []

        #if start_date:
        #    url += "&startDate=%s" % start_date.isoformat()
        #if offset:
        #    url += "&offset=%s" % offset
            
        for activity in self.load(self._url + '/activities'):
            out.append(Activity(id=activity["id"], name=activity["name"],
                access_token=self.access_token))

        return out

    def activity_stats(self, days=7):
        """Get number of activities, time, and distance for the past N days."""
        start = date.today() - timedelta(days=days)
        stats = defaultdict(float)
        
        for activity in self.activities(start_date=start):
            stats["activities"] += 1
            stats["moving_time"] += activity.detail.moving_time
            stats["distance"] += activity.detail.distance

        return stats
    
        
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
        self._name = kwargs['name']
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
            for effort in self.load("/activities/%s/efforts" % self.id):
                self._segments.append(Segment(effort))
        return self._segments


class ActivityDetail(StravaObject):
    
    def __init__(self, **kwargs):
        super(ActivityDetail, self).__init__(**kwargs)
        self._attr = self.load("/activities/%s" % kwargs['id'], 'activity')

    @property
    def athlete(self):
        return self._attr["athlete"]["name"]

    @property
    def athlete_id(self):
        return self._attr["athlete"]["id"]

    @property
    def bike(self):
        return self._attr["bike"]["name"]

    @property
    def bike_id(self):
        return self._attr["bike"]["id"]

    @property
    def location(self):
        return self._attr["location"]

    @property
    def distance(self):
        return self._attr["distance"]

    @property
    def average_speed(self):
        return self._attr["average_speed"]

    @property
    def moving_time(self):
        return self._attr["moving_time"]

    @property
    def average_watts(self):
        return self._attr["average_watts"]

    @property
    def maximum_speed(self):
        return self._attr["maximum_speed"]

    @property
    def elevation_gain(self):
        return self._attr["elevation_gain"]

    @property
    def description(self):
        return self._attr["description"]

    @property
    def commute(self):
        return self._attr["commute"]

    @property
    def trainer(self):
        return self._attr["trainer"]


class Segment(StravaObject):
    """Information about a single activity segment.

    Most of the data is encapsulated in a SegmentDetail instance, accessible via
    the "detail" property. This lets us lazy-load the details, and saves an API
    round-trip if all we care about is the ID or name of the segment.

    Note that this class combines the "effort" and "segment" as Strava defines
    them. They both ultimately pertain to a given portion of a activity, so it makes
    sense to access them both through the same interface.

    This does have the side effect, however, of requiring two API round-trips to
    load the "detail" property.  It's lazy-loaded, so if you just care about the
    segment name or ID, you won't take the it.
    """
    def __init__(self, attr):
        super(Segment, self).__init__(attr["id"])
        self._segment = attr["segment"]
        self._time = attr["elapsed_time"]
        self._detail = None
        
    @property
    def time(self):
        return self._time
    
    @property
    def name(self):
        return self._segment["name"]

    @property
    def detail(self):
        if not self._detail:
            self._detail = SegmentDetail(self._segment["id"], self.id)
        return self._detail


class SegmentDetail(StravaObject):
    def __init__(self, segment_id, effort_id):
        super(SegmentDetail, self).__init__(segment_id)
        self._effort_attr = self.load("/efforts/%s" % effort_id, "effort")
        self._segment_attr = self.load("/segments/%s" % segment_id, "segment")

    @property
    def distance(self):
        return self._segment_attr["distance"]

    @property
    def elapsed_time(self):
        return self._effort_attr["elapsedTime"]

    @property
    def moving_time(self):
        return self._effort_attr["movingTime"]

    @property
    def average_speed(self):
        return self._effort_attr["averageSpeed"]

    @property
    def maximum_speed(self):
        return self._effort_attr["maximumSpeed"]

    @property
    def average_watts(self):
        return self._effort_attr["averageWatts"]

    @property
    def average_grade(self):
        return self._segment_attr["averageGrade"]

    @property
    def climb_category(self):
        return self._segment_attr["climbCategory"]

    @property
    def elevations(self):
        return (self._segment_attr["elevationLow"],
                self._segment_attr["elevationHigh"],
                self._segment_attr["elevationGain"])
