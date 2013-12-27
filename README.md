textip
======

Check for your IP address on boot and send it as an SMS text using Twilio

## Usage
The python script 'textip.py' can be run at any time to check for your current IP address and send it as an SMS message.  You must first create a configuration file (e.g. twilio.conf) that contains:
- A valid Twilio Account SID
- A valid Twilio Authentication Token
- A valid Twilio Phone Number
- A recipient's phone number
In order for the script to execute on boot, create a link in /etc/network/if-post-up.d/ to the netwatch.sh bash script.  This script will monitor the /var/log/syslog file for an indication that an interface is listening on an IP address and then run the textip.py script.

Note that both scripts will require editing for your environment.  Specifically, the paths to the scripts and configuration file as well as which interface you specifically want to monitor.
