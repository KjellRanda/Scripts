#! /bin/bash
#
#RHOST="ftp.halifax.rwth-aachen.de"
#RBASE="fedora/linux"
#
#RHOST="ftp.uninett.no"
#RBASE="pub/linux/Fedora"
#
#RHOST="ftp.df.lth.se"
#RBASE="pub/fedora/linux"
#
#RHOST="mirrors.kernel.org"
#RBASE="mirrors/fedora"
#
#
#FHOST="download1.rpmfusion.org"
#FBASE=""
#
FHOST="ftp-stud.hs-esslingen.de"
FBASE=""
#
RHOST="ftp-stud.hs-esslingen.de"
RBASE="fedora/linux"
#
FED_HOME="/dl/repo/yum/Fedora"
FUS_HOME="/dl/repo/yum/Fedora-contrib/rpmfusion"
#
OPTS="-avrt --delete --no-motd"
#
echo "Downloading of repository data started at `date`"
#
VER="27 28"
ARCH="x86_64"
#
for i in $VER
do
   echo;echo;echo "Downloading F$i"
#
   for j in $ARCH
   do
      echo;echo "Downloading F$i $j Cloud ..."
      if [ $i -eq 27 ]
      then
         CI="CloudImages"
      else
	 CI="Cloud"
      fi
      [ ! -d $FED_HOME/releases/$i/$CI/$j ] && mkdir -p $FED_HOME/releases/$i/$CI/$j
      rsync --exclude 'debug' --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/$CI/$j/ $FED_HOME/releases/$i/$CI/$j
#
      echo;echo "Downloading F$i $j Docker ..."
      if [ $i -eq 27 ]
      then
	 DO="Docker"
      else
	 DO="Container"
      fi
      [ ! -d $FED_HOME/releases/$i/$DO/$j ] && mkdir -p $FED_HOME/releases/$i/$DO/$j
      rsync --exclude 'debug' --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/$DO/$j/ $FED_HOME/releases/$i/$DO/$j
#
      echo;echo "Downloading F$i $j Everything ..."
      [ ! -d $FED_HOME/releases/$i/Everything/$j/os ] && mkdir -p $FED_HOME/releases/$i/Everything/$j/os
      rsync --exclude 'debug' --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/Everything/$j/os/ $FED_HOME/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i $j Server ..."
      [ ! -d $FED_HOME/releases/$i/Server/$j ] && mkdir -p $FED_HOME/releases/$i/Server/$j
      rsync --exclude 'debug' --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/Server/$j/ $FED_HOME/releases/$i/Server/$j
#
      echo;echo "Downloading F$i $j Workstation ..."
      [ ! -d $FED_HOME/releases/$i/Workstation/$j ] && mkdir -p $FED_HOME/releases/$i/Workstation/$j
      rsync --exclude 'debug' --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/Workstation/$j/ $FED_HOME/releases/$i/Workstation/$j
#
      echo;echo "Downloading F$i $j Spins ..."
      [ ! -d $FED_HOME/releases/$i/Spins/$j ] && mkdir -p $FED_HOME/releases/$i/Spins/$j
      rsync --exclude 'debug'  --exclude 'drpms' $OPTS rsync://$RHOST/$RBASE/releases/$i/Spins/$j/ $FED_HOME/releases/$i/Spins/$j
   done
#
   for j in $ARCH
   do
      echo;echo "Downloading F$i $j updates ..."
      if [ $i -eq 27 ]
      then
	 PH=""
      else
	 PH="Everything"
      fi
      [ ! -d  $FED_HOME/updates/$i/$PH/$j ] && mkdir -p $FED_HOME/updates/$i/$PH/$j
      rsync $OPTS --exclude 'debug'  --exclude 'drpms' rsync://$RHOST/$RBASE/updates/$i/$PH/$j/ $FED_HOME/updates/$i/$PH/$j
   done
#
   for j in $ARCH
   do
      echo;echo "Downloading F$i rpmfusion free $j Everything ..."
      [ ! -d $FUS_HOME/free/fedora/releases/$i/Everything/$j/os ] && mkdir -p $FUS_HOME/free/fedora/releases/$i/Everything/$j/os
      rsync $OPTS --exclude 'debug'  --exclude 'drpms' rsync://$FHOST$FBASE/rpmfusion/free/fedora/releases/$i/Everything/$j/os/ $FUS_HOME/free/fedora/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i rpmfusion free $j updates ..."
      [ ! -d $FUS_HOME/free/fedora/updates/$i/$j ] && mkdir -p $FUS_HOME/free/fedora/updates/$i/$j
      rsync $OPTS --exclude 'debug'  --exclude 'drpms' rsync://$FHOST$FBASE/rpmfusion/free/fedora/updates/$i/$j/ $FUS_HOME/free/fedora/updates/$i/$j/
#
      echo;echo "Downloading F$i rpmfusion nonfree $j Everything ..."
      [ ! -d $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os ] && mkdir -p $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os
      rsync $OPTS --exclude 'debug'  --exclude 'drpms' rsync://$FHOST$FBASE/rpmfusion/nonfree/fedora/releases/$i/Everything/$j/os/ $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i rpmfusion nonfree $j updates ..."
      [ ! -d $FUS_HOME/nonfree/fedora/updates/$i/$j ] && mkdir -p $FUS_HOME/nonfree/fedora/updates/$i/$j
      rsync $OPTS --exclude 'debug'  --exclude 'drpms' rsync://$FHOST$FBASE/rpmfusion/nonfree/fedora/updates/$i/$j/ $FUS_HOME/nonfree/fedora/updates/$i/$j/
   done
done
#
#
#
echo;echo "Setting file permissions ..."
chown -R apache.apache $FED_HOME
chown -R apache.apache $FUS_HOME
chown -R apache.apache /dl/repo/yum/Local
#
echo;echo "Cleanup ..."
find /dl/repo/yum/logs -mtime +30 -exec rm -f {} \;
#
echo;echo "Downloading of repository data finished at `date`"
#
