#! /bin/bash
#
BCK_HOME="/dl/scratch/backup"
#
chown -R anonuid:backup $BCK_HOME
find $BCK_HOME -type d -exec chmod 2750 {} \;
find $BCK_HOME -type f -exec chmod 640 {} \;
#
