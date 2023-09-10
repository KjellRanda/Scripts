#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BACKUP_HOME="/data/homeassistant/backups"
ECHO="/bin/echo"
LS="/bin/ls"
RM="/bin/rm"
#
shopt -s nullglob
logfiles=($BACKUP_HOME/*)
N_FILES=$($ECHO ${#logfiles[@]})
#
MIN_FILES=30
MAX_AGE="+30"
#
if [ $N_FILES -ge $MIN_FILES ]
then
   find $BACKUP_HOME -maxdepth 1 -type f -mtime $MAX_AGE | while read -r file; do
      $ECHO "Removing backup file $file"
      sudo $RM -f $file
   done
else
   $ECHO ""
   $ECHO "Only $N_FILES backup files exsist. None removed."
   $ECHO ""
fi
