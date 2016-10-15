#!/bin/bash

cd /data/git/PDD/PDD
./PDD.py

RES=`grep ^Result forklift.log | tail -1 | cut -f 2 -d ' '`
[ "${RES}" = 'OK' ] && firefox
