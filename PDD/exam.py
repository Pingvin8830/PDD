#!/bin/python3

from os  import getcwd
from sys import path as PATH
PATH.append (getcwd () + '/moduls')

from gui import main

main ()
