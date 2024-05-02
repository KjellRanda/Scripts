#! /bin/bash
#
RM="/bin/rm"
ECHO="/bin/echo"
#
RCLONE="/data/rclone/rclone-prod/rclone"
#
LOGDIR="/data/rclone"
dirdate=$(date +'%Y.%m.%d')
LOGFILE="$LOGDIR/$dirdate-rclone-backup.log"
#
#PARAM="--retries 1 --low-level-retries 1 --ignore-errors --drive-pacer-min-sleep 120ms --links --drive-pacer-burst=75 --local-no-check-updated"
PARAM="--ignore-errors --links --retries 2 --low-level-retries 5"
#
EXCL1="/data/python/prod/exclude.list"
#
sudo $RCLONE -v sync --exclude-from $EXCL1 $PARAM --log-file $LOGFILE /data GoogleDrive:Gulen-backup/rclone/data
sleep 60
sudo $RCLONE -v sync                       $PARAM --log-file $LOGFILE /home GoogleDrive:Gulen-backup/rclone/home
sleep 60
sudo $RCLONE -v sync                       $PARAM --log-file $LOGFILE /etc  GoogleDrive:Gulen-backup/rclone/etc
#
shopt -s nullglob
logfiles=($LOGDIR/*-rclone-backup.log)
N_FILES=$($ECHO ${#logfiles[@]})
#
MIN_FILES=10
MAX_AGE="+10"
#
if [ $N_FILES -ge $MIN_FILES ]
then
   find $LOGDIR -maxdepth 1 -name "*-rclone-backup.log" -mtime $MAX_AGE | while read -r file; do
      $ECHO "Removing log file $file"
      sudo $RM -f $file
   done
else
   $ECHO ""
   $ECHO "Only $N_FILES log files exsist. None removed."
   $ECHO ""
fi