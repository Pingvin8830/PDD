#!/bin/bash

cd /data/git/PDD/PDD
./exam.py -c configs/PDD.conf

RES=`grep ^Result logs/PDD.log | tail -1 | cut -f 2 -d ' '`
if [ "${RES}" != 'OK' ]; then
  notify-send "Нет билета - нет интернета."
  exit
  fi

./exam.py -c configs/expluatation.conf
RES=`grep ^Result logs/expluatation.log | tail -1 | cut -f 2 -d ' '`
[ "${RES}" = 'OK' ] && firefox
