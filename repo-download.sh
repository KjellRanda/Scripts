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
VER="23 24"
ARCH="x86_64"
#
for i in $VER
do
   echo;echo;echo "Downloading F$i"
#
   for j in $ARCH
   do
      echo;echo "Downloading F$i $j Cloud ..."
      if [ $i -eq 21 ]
      then
         [ ! -d $FED_HOME/releases/$i/Cloud/Images/$j ] && mkdir -p     $FED_HOME/releases/$i/Cloud/Images/$j
         rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Cloud/Images/$j/ $FED_HOME/releases/$i/Cloud/Images/$j
      fi
      if [ $i -eq 23 ]
      then
         [ ! -d $FED_HOME/releases/$i/Cloud/$j ] && mkdir -p     $FED_HOME/releases/$i/Cloud/$j
         rsync $OPTS --exclude 'debug' rsync://$RHOST/$RBASE/releases/$i/Cloud/$j/ $FED_HOME/releases/$i/Cloud/$j
      fi
      if [ $i -eq 24 ]
      then
         [ ! -d $FED_HOME/releases/$i/CloudImages/$j ] && mkdir -p     $FED_HOME/releases/$i/CloudImages/$j
         rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/CloudImages/$j/ $FED_HOME/releases/$i/CloudImages/$j
      fi

#
      if [ $i -eq 23 ]
      then
         echo;echo "Downloading F$i $j Cloud_Atomic ..."
	 [ ! -d $FED_HOME/releases/$i/Cloud_Atomic/$j ] && mkdir -p     $FED_HOME/releases/$i/Cloud_Atomic/$j
         rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Cloud_Atomic/$j/ $FED_HOME/releases/$i/Cloud_Atomic/$j
      fi
#
      echo;echo "Downloading F$i $j Docker ..."
      [ ! -d $FED_HOME/releases/$i/Docker/$j ] && mkdir -p     $FED_HOME/releases/$i/Docker/$j
      rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Docker/$j/ $FED_HOME/releases/$i/Docker/$j
#
      echo;echo "Downloading F$i $j Everything ..."
      [ ! -d $FED_HOME/releases/$i/Everything/$j/os ] && mkdir -p     $FED_HOME/releases/$i/Everything/$j/os
      rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Everything/$j/os/ $FED_HOME/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i $j Server ..."
      [ ! -d $FED_HOME/releases/$i/Server/$j ] && mkdir -p     $FED_HOME/releases/$i/Server/$j
      rsync --exclude 'debug' $OPTS rsync://$RHOST/$RBASE/releases/$i/Server/$j/ $FED_HOME/releases/$i/Server/$j
#
      echo;echo "Downloading F$i $j Workstation ..."
      [ ! -d $FED_HOME/releases/$i/Workstation/$j ] && mkdir -p     $FED_HOME/releases/$i/Workstation/$j
      rsync --exclude 'debug' $OPTS rsync://$RHOST/$RBASE/releases/$i/Workstation/$j/ $FED_HOME/releases/$i/Workstation/$j
   done
#
   echo;echo "Downloading F$i live CDs ..."
   if [ $i -eq 23 ]
   then
      [ ! -d $FED_HOME/releases/$i/Live/$j ] &&     mkdir -p $FED_HOME/releases/$i/Live/$j 
      rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Live/$j/ $FED_HOME/releases/$i/Live/$j
   fi
   if [ $i -eq 24 ]
   then
      [ ! -d $FED_HOME/releases/$i/Spins/$j ] &&     mkdir -p $FED_HOME/releases/$i/Spins/$j
      rsync $OPTS rsync://$RHOST/$RBASE/releases/$i/Spins/$j/ $FED_HOME/releases/$i/Spins/$j
   fi

#
   for j in $ARCH
   do
      echo;echo "Downloading F$i $j updates ..."
      [ ! -d  $FED_HOME/updates/$i/$j ] && mkdir -p                      $FED_HOME/updates/$i/$j
      rsync $OPTS --exclude 'debug' rsync://$RHOST/$RBASE/updates/$i/$j/ $FED_HOME/updates/$i/$j/
   done
#
   for j in $ARCH
   do
      echo;echo "Downloading F$i rpmfusion free $j Everything ..."
      [ ! -d $FUS_HOME/free/fedora/releases/$i/Everything/$j/os ] && mkdir -p                                $FUS_HOME/free/fedora/releases/$i/Everything/$j/os
      rsync $OPTS --exclude 'debug' rsync://$FHOST$FBASE/rpmfusion/free/fedora/releases/$i/Everything/$j/os/ $FUS_HOME/free/fedora/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i rpmfusion free $j updates ..."
      [ ! -d $FUS_HOME/free/fedora/updates/$i/$j ] && mkdir -p                                $FUS_HOME/free/fedora/updates/$i/$j
      rsync $OPTS --exclude 'debug' rsync://$FHOST$FBASE/rpmfusion/free/fedora/updates/$i/$j/ $FUS_HOME/free/fedora/updates/$i/$j/
#
      echo;echo "Downloading F$i rpmfusion nonfree $j Everything ..."
      [ ! -d $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os ] && mkdir -p                                $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os
      rsync $OPTS --exclude 'debug' rsync://$FHOST$FBASE/rpmfusion/nonfree/fedora/releases/$i/Everything/$j/os/ $FUS_HOME/nonfree/fedora/releases/$i/Everything/$j/os/
#
      echo;echo "Downloading F$i rpmfusion nonfree $j updates ..."
      [ ! -d $FUS_HOME/nonfree/fedora/updates/$i/$j ] && mkdir -p                                $FUS_HOME/nonfree/fedora/updates/$i/$j
      rsync $OPTS --exclude 'debug' rsync://$FHOST$FBASE/rpmfusion/nonfree/fedora/updates/$i/$j/ $FUS_HOME/nonfree/fedora/updates/$i/$j/
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
