#!/bin/bash

#setup
host='localhost'
port='8181'
#idx for download, upload and ping
idxdl=71
idxul=72
idxpng=73
idxbb=74

# speedtest server number
# serverst=xxxx

# no need to edit
# speedtest-cli --simple --server $serverst > outst.txt
output='/tmp/speedtest.txt'
#speedtest-cli --server 31861 --simple > $output
#speedtest-cli --simple > $output
speedtest-cli > $output

download=$(cat $output | sed -ne 's/^Download: \([0-9]*\.[0-9]*\).*/\1/p')
upload=$(cat $output | sed -ne 's/^Upload: \([0-9]*\.[0-9]*\).*/\1/p')
#png=$(cat $output | sed -ne 's/^Ping: \([0-9]*\.[0-9]*\).*/\1/p')
png=$(cat $output | grep "Hosted by" | cut -d : -f2 | awk '{print $1}')

site=$(cat $output | grep "Hosted by " | sed 's/Hosted by //' | cut -d'[' -f1 | sed 's/ *$//')
dist=$(cat $output | grep "Hosted by " | cut -d'[' -f2 | cut -d']' -f1 | sed 's/km//' | sed 's/ *$//')
from=$(cat $output | grep "Testing from " | sed 's/Testing from //' | cut -d'(' -f1 | sed 's/ *$//')
ipad=$(cat $output | grep "Testing from " | cut -d'(' -f2 | cut -d')' -f1)

# output if you run it manually
#echo "Download = $download Mbps"
#echo "Upload =  $upload Mbps"
#echo "Ping =  $png ms"

# Updating download, upload and ping ..
wget -q --delete-after "http://$host:$port/json.htm?type=command&param=udevice&idx=$idxdl&svalue=$download" >/dev/null 2>&1
wget -q --delete-after "http://$host:$port/json.htm?type=command&param=udevice&idx=$idxul&svalue=$upload" >/dev/null 2>&1
wget -q --delete-after "http://$host:$port/json.htm?type=command&param=udevice&idx=$idxpng&svalue=$png" >/dev/null 2>&1

# Reset Broadband switch
wget -q --delete-after "http://$host:$port/json.htm?type=command&param=udevice&idx=$idxbb&svalue=0" >/dev/null 2>&1

# Domoticz logging
wget -q --delete-after "http://$host:$port/json.htm?type=command&param=addlogmessage&message=speedtest.net-logging" >/dev/null 2>&1
#
python /usr/local/bin/speed.py -d "$download" -u "$upload" -p "$png"
