#! /bin/bash
#
SECRET=$(kubectl -n kube-system get secret | grep metric | awk '{print $1}')
TOKEN=$(kubectl -n kube-system describe secret $SECRET | grep token: | awk '{print $2}')
/bin/echo $TOKEN
