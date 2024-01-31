#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BACKUP_HOME="/dl/scratch/backup/grafana"
ECHO="/bin/echo"
RM="/bin/rm"
#
grafana-backup save
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
   find $BACKUP_HOME -type f -mtime $MAX_AGE | while read -r ffile; do
      $ECHO "Removing backup file $ffile"
      $RM -f $ffile
   done
else
   $ECHO ""
   $ECHO "Only $N_FILES backup files exsist. None removed."
   $ECHO ""
fi
#
rclone -v sync --exclude grafana.log --log-file $BACKUP_HOME/grafana.log $BACKUP_HOME  GoogleDrive:Grafana
