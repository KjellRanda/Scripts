#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BACKUP_HOME="/data/homeassistant/backups"
ECHO="/bin/echo"
RM="/bin/rm"
PING="/usr/bin/ping"
#
NFSHOST="nazgul.net.home"
BCKDIR="/dl/scratch"
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
#
$PING -W 2 -c 1 $NFSHOST > /dev/null
if [ "$?" == "0" ]
then
   $ECHO ""
   $ECHO "Host $NFSHOST is online. Copying HA backup files"
   $ECHO ""
   sudo mount -t nfs $NFSHOST:$BCKDIR $BCKDIR
   sudo rsync -vrt --delete $BACKUP_HOME/ $BCKDIR/backup/HA
   sudo find  $BCKDIR/backup/HA -type f -exec sudo chmod 640 {} \; 
   sudo umount $BCKDIR
else
   $ECHO ""
   $ECHO "Host $NFSHOST if offline. HA backupfiles not saved to external storage"
   $ECHO ""
fi
