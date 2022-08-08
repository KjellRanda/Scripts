#! /bin/bash
#
rclone -v sync --exclude-from exclude.list --log-file transfer.log /dl/picture           GoogleDrive:Bilder
rclone -v sync                             --log-file transfer.log /dl/mp3/CD-collection GoogleDrive:mp3
rclone -v sync                             --log-file transfer.log /dl/documents         GoogleDrive:Documents
