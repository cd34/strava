#!/usr/bin/env python

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__))))), 'strava.cfg')))

from strava import Athlete

st = Athlete(access_token=config.get('user', 'access_token'))
athlete = st.athlete

print 'Athlete ID: {id}'.format(id=athlete['id'])
print '{firstname} {lastname}'.format(firstname=athlete['firstname'],
    lastname=athlete['lastname'])
print 'Sex: {sex}'.format(sex=athlete['sex'])
print 'From: {city}, {state} {country}'.format(city=athlete['city'], 
    state=athlete['state'], country=athlete['country'])
print 'Email: {email}'.format(email=athlete['email'])
print 'Profile URL: {profile}'.format(profile=athlete['profile'])

print '{friends} friends, {follower} followers'.format(
    friends=athlete['friend_count'], follower=athlete['follower_count'])

for shoe in athlete['shoes']:
    print '  Shoe: {shoe} Distance {distance}'.format(shoe=shoe['name'],
        distance=shoe['distance'])

for bike in athlete['bikes']:
    print '  Bike: {bike} Distance: {distance}'.format(bike=bike['name'],
        distance=bike['distance'])

for club in athlete['clubs']:
    print '  Club: {club} ID: {id}'.format(club=club['name'],
        id=club['id'])
