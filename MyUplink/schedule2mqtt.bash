#! /bin/bash
#
MyUplink_HOME="/data/MyUplink"
#
. /home/pi/.bashrc
cd $MyUplink_HOME
#
python schedule2mqtt.py >> $MyUplink_HOME/schedule2mqtt.errlog 2>&1
#