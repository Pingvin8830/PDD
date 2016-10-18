#!/bin/bash

cd /data/git/PDD/PDD
./exam.py

RES=`grep ^Result logs/forklift.log | tail -1 | cut -f 2 -d ' '`
[ "${RES}" = 'OK' ] && firefox
