Instructions for generating single token for testing
====================================================

* Create an App in Strava https://www.strava.com/settings/api

* Copy strava.cfg.sample to strava.cfg and fill in the appropriate
values

* Run the authorize script which will redirect to a url.
Pick out the &code= variable and run the token exchange
script which will return an access code. You can modify
the token exchange to print the athlete data if you want.

Sample workflow
===============

./oauth2_authorize.py

Paste the URL in the browser, authorize the application.
You'll be redirected to the location specified in your strava.cfg

oauth2_token_exchange.py 12345

This will generate an access_token and you should be able to visit
http://www.strava.com/settings/apps and see that your app has been
added.

Take the access_token and place it in your strava.cfg file in its
own section so that you can use it to do API calls from within your app.
That access token needs to be used to fetch data from Strava's API.
