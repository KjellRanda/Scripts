#! /bin/bash
#
PWR_HOME="/data/python/prod"
PWR_PRICE="/data/powerprice"
PWR_TMP="/powerprice.new"
PWR_OK="powerprice.list"
#
MV="/usr/bin/mv"
RM="/usr/bin/rm"
#
. /home/pi/.bashrc
cd $PWR_HOME
#
python powerprice.py NO5 > $PWR_PRICE/$PWR_TMP
#
if [ $? -eq 0 ]
then
    $MV -f $PWR_PRICE/$PWR_TMP $PWR_PRICE/$PWR_OK
else
    $RM -f $PWR_PRICE/$PWR_TMP
fi
#