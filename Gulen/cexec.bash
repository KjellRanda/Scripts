#! /bin/bash
#
ECHO="/bin/echo"
CMD="/bin/bash"
#
usage()
{
    $ECHO ""
    $ECHO "Usage - $0 <containername> [<command>]"
    $ECHO ""
    exit 1
}
#
[ $# -ne 1 ] && [ $# -ne 2 ] && usage
#
nc=$(docker ps | grep -c "$1")
if [ "$nc" -eq 1 ]
then
	id=$(docker ps | grep "$1" | awk '{print $1}')
   [ $# -eq 2 ] && CMD="$2"
   docker exec --tty -it "$id" "$CMD"
else
   $ECHO ""
   $ECHO "Containername not unique or not found"
   usage
fi
