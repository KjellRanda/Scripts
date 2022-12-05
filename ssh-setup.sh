#!/bin/bash
# 
#
PROG=`basename $0`
#
if [ -d "${HOME}/.ssh" ]
then
     echo " "
     echo "$PROG: Cannot continue. You already have a .ssh directory under ${HOME}."
     echo " "
     echo "    Please rename or delete ${HOME}/.ssh (mv ${HOME}/.ssh ${HOME}/.ssh-old), then run once more."
     echo " "
     exit 1
fi
mkdir "${HOME}/.ssh" || exit 2
cd "${HOME}/.ssh" || exit 2

touch authorized_keys2 && ln authorized_keys2 authorized_keys || exit 2

for i in "rsa" "dsa"
do
     echo "$PROG: Creating ssh keys ($i). Please wait ...."
     ssh-keygen -f "id_${i}" -t $i -N "" < /dev/null > /dev/null
     if [ ! -f "id_${i}.pub" ]
     then
           echo "$PROG: ${HOME}/.ssh/id_${i}.pub keyfile not created. Exiting..."
           exit 2
     fi
     cat "id_${i}.pub" >> authorized_keys2
done

cat > config <<EOF
     StrictHostKeyChecking no
     ForwardX11 no
EOF

chmod g-ws,o-w "$HOME"
chmod g-ws,o-rwx .
chmod u=rw,og= *
