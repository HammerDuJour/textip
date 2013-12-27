#!/bin/bash

LOGFILE="/home/pi/tools/netwatch_log.txt"
TIME=$(date +%b' '%d' '%T)
LOGPREFIX="$TIME ****netwatch: "

PSCOUNT=$(ps -A | grep netwatch.sh | grep -v grep | wc -l)
# This script creates two processes. The second is created when tail starts.
# There is also a tail process so go figure.
if [ $PSCOUNT -gt "2" ]; then
    echo $LOGPREFIX "attempted to start when already running" >> $LOGFILE
    exit 1
fi

echo $LOGPREFIX "starting" > $LOGFILE

tail -fn0 /var/log/syslog | \
while read line ; do
    echo "$line" | grep "wlan0" >> $LOGFILE
    echo "$line" | egrep "Listen normally.*wlan0" > /dev/null
    if [ $? = 0 ]
    then
        echo $LOGPREFIX "listen found" >> $LOGFILE
        /home/pi/tools/textip.py &>> $LOGFILE
        exit 0
    fi
done
echo "netwatch: stopping" >> /home/pi/tools/netwatch_log.txt
