#! /bin/bash
#
BCK_HOME="/dl/scratch/backup"
#
rclone -v sync --log-file $BCK_HOME/backup.log --include nazgul-*     $BCK_HOME GoogleDrive:Linux-backup/Nazgul
rclone -v sync --log-file $BCK_HOME/backup.log --include eagle-*      $BCK_HOME GoogleDrive:Linux-backup/Eagle
rclone -v sync --log-file $BCK_HOME/backup.log --include hobbit-*     $BCK_HOME GoogleDrive:Linux-backup/Hobbit
rclone -v sync --log-file $BCK_HOME/backup.log --include gatekeeper-* $BCK_HOME GoogleDrive:Linux-backup/Gatekeeper
