#! /bin/bash
#
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ECHO="/bin/echo"
#
CONTAINER="influxdb"
#
nc=$(docker ps | grep -c $CONTAINER)
if [ "$nc" -eq 1 ]
then
	ID=$(docker ps | grep $CONTAINER | awk '{print $1}')
else
   $ECHO ""
   $ECHO "Container $CONTAINER not found"
   $ECHO ""
   exit 1
fi
#
dirdate=$(date +'%d.%m.%Y')
#
docker exec -t "$ID" mkdir /opt/$#dirdate#
docker exec -t "$ID" influxd backup --portable /opt/"$dirdate"
#
