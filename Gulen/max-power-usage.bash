#! /bin/bash
#
MAX_HOME="/data/python/prod"
#
# shellcheck disable=SC1091
#
. /home/pi/.bashrc
cd $MAX_HOME || exit
#
python max-power-usage.py
#
