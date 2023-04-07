#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ECHO="/bin/echo"
#
CONTAINER="influxdb"
#
nc=`docker ps | grep -c $CONTAINER`
if [ $nc -eq 1 ]
then
   ID=`docker ps | grep $CONTAINER | awk '{print $1}'`
else
   $ECHO ""
   $ECHO "Container $CONTAINER not found"
   $ECHO ""
   exit 1
fi
#
dirdate=$(date +'%d.%m.%Y')
#
docker exec -t $ID mkdir /opt/$dirdate
docker exec -t $ID influxd backup --portable /opt/$dirdate
#
BACKUP_HOME="/data/influxdb_backup"
ECHO="/bin/echo"
LS="/bin/ls"
RM="/bin/rm"
#
shopt -s nullglob
logfiles=($BACKUP_HOME/*)
N_FILES=$($ECHO ${#logfiles[@]})
#
MIN_FILES=10
MAX_AGE="+30"
#
if [ $N_FILES -ge $MIN_FILES ]
then
   find $BACKUP_HOME -maxdepth 1 -type d -mtime $MAX_AGE | while read -r bdir; do
      $ECHO "Removing backup folder $bdir"
      $RM -rf $bdir
   done
else
   $ECHO ""
   $ECHO "Only $N_FILES backup files exsist. None removed."
   $ECHO ""
fi
