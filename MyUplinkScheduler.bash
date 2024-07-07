#! /bin/bash
#
MyUplink_HOME="/data/MyUplink"
#
. /home/pi/.bashrc
cd $MyUplink_HOME
#
python MyUplinkScheduler.py >> $MyUplink_HOME/MyUplinkScheduler.errlog 2>&1
#