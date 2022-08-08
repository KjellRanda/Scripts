#! /bin/bash
#
rclone -v sync --log-file /home/dogbert/rclone/unifi_backup.log /usr/share/unifi/data/backup/autobackup  GoogleDrive:Unify_backup
