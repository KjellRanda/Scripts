#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
BACKUP_HOME="/var/opt/gitlab/backups"
ECHO="/bin/echo"
RM="/bin/rm"
#
gitlab-backup create
#
rclone -v sync --log-file /dl/scratch/backup/gitlab/gitlab.log $BACKUP_HOME GoogleDrive:Gitlab
rclone -v sync --log-file /dl/scratch/backup/gitlab/gitlab.log /etc/gitlab  GoogleDrive:Gitlab-etc
