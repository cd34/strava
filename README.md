strava
======

I'm currently evaluating the (recently released in BETA) Strava 3.0 API to see if this project 
an be adapted to work with it.  I'm cautiously optimistic that something can be worked out.

-- packetslave (2014/01/06)

Installation Instructions
=========================

virtualenv projectname
cd projectname
source bin/activate
easy_install http://github.com/cd34/strava/tarball/master
cp -Rp ../../examples examples
cd examples
cp strava.cfg.sample strava.cfg
edit strava.cfg
cp -Rp ../../oauth_setup oauth_setup
cd oauth_setup
./oauth2_authorize.py
copy URL, visit in browser
Grab &code= variable from redirected URL
./oauth2_token_exchange.py code_value
insert access_token from script in strava.cfg

    [user]
    access_token =
