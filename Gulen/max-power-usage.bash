#! /bin/bash
#
MAX_HOME="/data/python/prod"
#
. /home/pi/.bashrc
cd $MAX_HOME || exit
#
python max-power-usage.py
#
