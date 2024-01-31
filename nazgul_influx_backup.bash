#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BACKUP_HOME="/dl/scratch/backup/influxdb"
ECHO="/bin/echo"
RM="/bin/rm"
#
dirdate=$(date +'%d.%m.%Y')
#
mkdir  -p $BACKUP_HOME/$dirdate
influxd backup --portable /$BACKUP_HOME/$dirdate
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
#
rclone -v sync --log-file $BACKUP_HOME/influxdb.log $BACKUP_HOME  GoogleDrive:Influxdb
