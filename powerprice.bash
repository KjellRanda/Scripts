#! /bin/bash
#
PWR_HOME="/data/python/prod"
PWR_PRICE="/data/powerprice"
PWR_TMP="/powerprice.new"
PWR_TSORT="powerprice.sorted"
PWR_OK="powerprice.list"
#
MV="/usr/bin/mv"
RM="/usr/bin/rm"
ECHO="/usr/bin/echo"
#
. /home/pi/.bashrc
cd $PWR_HOME
#
if [ -r $PWR_PRICE/$PWR_OK ]
then
   NTOT=$(wc -l $PWR_PRICE/$PWR_OK | cut  -d' ' -f1) 
   NTD=$(grep -c "^$(date --date=today    '+%Y-%m-%d')" $PWR_PRICE/$PWR_OK)
   NTM=$(grep -c "^$(date --date=tomorrow '+%Y-%m-%d')" $PWR_PRICE/$PWR_OK)
#
   if [ $NTOT -eq 49 -a $NTD -eq 24 -a $NTM -eq 24 ]
   then
      $ECHO "Powerprice file $PWR_PRICE/$PWR_OK is already up to date"
      exit
   else
      $ECHO "Powerprice file $PWR_PRICE/$PWR_OK is outdated. Creating new"
   fi
else
   $ECHO "Powerprice file $PWR_PRICE/$PWR_OK not found. Creating new"
fi
#
python powerprice.py NO5 > $PWR_PRICE/$PWR_TMP
#
if [ $? -eq 0 ]
then
    (head -n 1 $PWR_PRICE/$PWR_TMP && tail -n +2 $PWR_PRICE/$PWR_TMP | sort) > $PWR_PRICE/$PWR_TSORT
    if [ $? -eq 0 ]
    then
       $MV -f $PWR_PRICE/$PWR_TSORT $PWR_PRICE/$PWR_OK
       $RM -f $PWR_PRICE/$PWR_TMP
    else
       $RM -f $PWR_PRICE/$PWR_TMP $PWR_PRICE/$PWR_TSORT
    fi
else
    $RM -f $PWR_PRICE/$PWR_TMP
fi
#
