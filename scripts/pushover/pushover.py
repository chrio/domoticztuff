#!/usr/bin/python
# send pushover notifications from the command line

import sys

if len(sys.argv) > 1:
    print "Sending message: " + sys.argv[1]

    USER_KEY = "<userkey here>"
    APP_TOKEN= "<apptoken here>"
    
    import httplib, urllib
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": APP_TOKEN,
                "user": USER_KEY,
                "message": sys.argv[1],
                }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

