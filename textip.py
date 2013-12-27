#! /usr/bin/env python

import sys
import subprocess
import urllib
import urllib2
import xml.etree.ElementTree as ET

if len(sys.argv) > 1:
    ifname = sys.argv[1]
else:
    ifname = 'wlan0'

proc = subprocess.Popen(['ifconfig',ifname], stdout=subprocess.PIPE)
ifinfo = proc.stdout.read()

addstart = ifinfo.find('inet addr:')
if addstart < 0:
    print ifname + ' is not connected.'
else:
    bcaststart = ifinfo.find('Bcast:')
    ipaddr = ifinfo[addstart:bcaststart]

    print ipaddr

# Twilio stuff
# You must have a file listed below that contains 4 lines for:
# Twilio Account SID
# Twilio Authentication Token
# Twilio Phone Number
# Recipient Phone Number
    twilioConfigFile = '/home/pi/tools/twilio.conf'
    params = [line.strip() for line in open(twilioConfigFile)]
    if len(params) >= 4:
        accountSid = params[0]
        authToken = params[1]
        fromNum = params[2]
        toNum = params[3]

    baseUrl = 'https://api.twilio.com/2010-04-01/Accounts/' + \
        accountSid +  '/SMS/Messages'
    parameters = {'From' : fromNum,
                  'To' : toNum,
                  'Body' : ipaddr}

    data = urllib.urlencode(parameters)
    req = urllib2.Request(baseUrl, data)
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, baseUrl, accountSid, authToken)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)

# Install the opener.
# Now all calls to urllib2.urlopen use the opener.
    urllib2.install_opener(opener)

    response = urllib2.urlopen(req)
    result = response.read()
    
    resultElements = ET.ElementTree(ET.fromstring(result))
    resultRoot = resultElements.getroot()
    for status in resultRoot.iter('Status'):
        print 'Msg Status: ' + status.text

