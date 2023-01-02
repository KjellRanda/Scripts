#! /bin/bash
#
printf "%-20s  %-9s %-8s\n" "Mountpoint" "Dev" "Ver"
printf "%0.s=" {1..35}
printf "\n"
#
for i in $(grep xfs /etc/fstab | grep -v "^#" | awk '{print $1}'| cut -d= -f2)
do
	mnt=$(grep "$i" /etc/fstab | grep -v "^#" | awk '{print $2}')
	if [ -e /dev/disk/by-uuid/"$i" ]
	then
		dev=$(ls -la /dev/disk/by-uuid/"$i" | awk '{print $11}' | sed 's/..\/..\///')
	else
		dev=$(ls -la "$i" | awk '{print $11}' | sed 's/..\///')
	fi
	ver=$(grep XFS /var/log/messages | grep Mounting | grep \($dev\) | cut -d"(" -f2 | sort -u | awk '{print $3}')
	printf "%-20s  %-9s %-8s\n" "$mnt" "$dev" "$ver"
done 
