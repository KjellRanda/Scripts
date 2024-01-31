#! /bin/bash
#
cd /home/dogbert/rclone
#
rclone -v sync --log-file git.log /home/dogbert/MyWeatherStation                           GoogleDrive:Git/MyWeatherStation
rclone -v sync --log-file git.log /home/dogbert/Scripts                                    GoogleDrive:Git/Scripts
rclone -v sync --log-file git.log /home/dogbert/flowercare                                 GoogleDrive:Git/flowercare
rclone -v sync --log-file git.log /home/dogbert/miflora                                    GoogleDrive:Git/miflora
rclone -v sync --log-file git.log /home/dogbert/abuse                                      GoogleDrive:Git/abuse
rclone -v sync --log-file git.log /home/dogbert/nagiosplug-1.3-beta1/plugins/sensor-plugin GoogleDrive:Git/sensor-plugin
