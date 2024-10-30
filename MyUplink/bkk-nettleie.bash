#! /bin/bash
#
PWR_HOME="/data/python/prod"
PWR_PRICE="/data/powerprice"
PWR_TMP="/nettleie.new"
PWR_OK="nettleie.bkk"
#
MV="/usr/bin/mv"
RM="/usr/bin/rm"
#
. /home/pi/.bashrc
cd $PWR_HOME
#
python bkk-nettleie.py > $PWR_PRICE/$PWR_TMP
#
if [ $? -eq 0 ]
then
    $MV -f $PWR_PRICE/$PWR_TMP $PWR_PRICE/$PWR_OK
else
    $RM -f $PWR_PRICE/$PWR_TMP
fi
#