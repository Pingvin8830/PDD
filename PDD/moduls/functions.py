#!/bin/python3

from config   import settings as CONF
from datetime import datetime

def set_var ():
  global CON
  global CUR
  write_log ('Vars set at start values')
  write_log ('''
FONT:     %s
DATABASE: %s
IMAGE:    %s
WINDOW:   %s, %s
''' % (
  (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')),
  CONF.get ('FILES', 'db'),
  CONF.get ('FILES', 'tmp'),
  CONF.get ('WINDOW', 'title'), '%dx%d+%d+%d' % (CONF.getint ('WINDOW', 'width'), CONF.getint ('WINDOW', 'height'), CONF.getint ('WINDOW', 'x_step'), CONF.getint ('WINDOW', 'y_step'))
  ), False
             )

def write_image (data):
  file = open (CONF.get ('FILES', 'tmp'), 'wb')
  file.write (data)
  file.close ()
  write_log ('Image write')

def write_log (string, date = True):
  while len (string) < 60:
    string += ' '
  file = open (CONF.get ('FILES', 'log'), 'a', encoding = 'utf-8')
  file.write (string)
  if date:
    file.write (' %s\n' % datetime.today ())
  else:
    file.write ('\n')
  file.close ()
  
