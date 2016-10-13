#!/bin/bash

./PDD.py

RES=`grep ^Result PDD.log | tail -1 | cut -f 2 -d ' '`

while [ "${RES}" != 'OK' ]; do
  ./PDD.py
  RES=`grep ^Result PDD.log | tail -1 | cut -f 2 -d ' '`
  done

echo 'firefox'
