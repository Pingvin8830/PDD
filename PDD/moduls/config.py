#!/bin/python3

from configparser import RawConfigParser
from os           import getcwd
from sys          import argv
from sys          import path     as PATH
from sys          import platform as OS

FILE = None
for i in range (len (argv)):
  if argv [i] == '-c' or argv [i] == '--conf':
    try:    FILE = argv [i + 1]
    except: print ('Файл конфигурации указан неверно.')
    
PWD = getcwd ()

class MyConf (RawConfigParser):
  '''Мой конфигурационник'''
  def __init__ (self, file = None):
    super (MyConf, self).__init__ ()
    self.CONF_FILE = file
    if not self.CONF_FILE:
      if   OS == 'linux': self.CONF_FILE = PWD + '/configs/PDD.conf'
      elif OS == 'win32': self.CONF_FILE = PWD + '/configs/PDD_win.conf'
    self.read (self.CONF_FILE)
    self.control_file ()

  def control_file (self):
    '''Проверяет наличие параметров в файле'''
    self.sections = ['FONT', 'FILES', 'WINDOW', 'TICKET', 'QUESTION', 'ANSWER', 'LOGIC']
    for section in self.sections:
      if not self.has_section (section):
        self.add_section (section)
    if not self.has_option ('FONT',     'name'):      self.set ('FONT',     'name',      'Courier New')
    if not self.has_option ('FONT',     'size'):      self.set ('FONT',     'size',      14)
    if not self.has_option ('FILES',    'db'):        self.set ('FILES',    'db',        PWD + '/databases/forklift.db')
    if not self.has_option ('FILES',    'tmp'):       self.set ('FILES',    'tmp',       PWD + '/tmp/now.jpg')
    if not self.has_option ('FILES',    'log'):       self.set ('FILES',    'log',       PWD + '/logs/forklift.log')
    if not self.has_option ('WINDOW',   'title'):     self.set ('WINDOW',   'title',     'Программа проведения тестов')
    if not self.has_option ('WINDOW',   'width'):     self.set ('WINDOW',   'width',     850)
    if not self.has_option ('WINDOW',   'height'):    self.set ('WINDOW',   'height',    900)
    if not self.has_option ('WINDOW',   'x_step'):    self.set ('WINDOW',   'x_step',    0)
    if not self.has_option ('WINDOW',   'y_step'):    self.set ('WINDOW',   'y_step',    0)
    if not self.has_option ('TICKET',   'count'):     self.set ('TICKET',   'count',     40)
    if not self.has_option ('TICKET',   'start'):     self.set ('TICKET',   'start',     1)
    if not self.has_option ('QUESTION', 'count'):     self.set ('QUESTION', 'count',     20)
    if not self.has_option ('QUESTION', 'start'):     self.set ('QUESTION', 'start',     1)
    if not self.has_option ('ANSWER',   'count'):     self.set ('ANSWER',   'count',     5)
    if not self.has_option ('ANSWER',   'start'):     self.set ('ANSWER',   'start',     1)
    if not self.has_option ('LOGIC',    'max_error'): self.set ('LOGIC',    'max_error', 2)
    
  def set (self, section, option, value):
    super (MyConf, self).set (section, option, value)
    with open (self.CONF_FILE, 'w') as conf:
      self.write (conf)

settings = MyConf (FILE)
if __name__ == '__main__':
  print ('Это всего-лишь модуль для работы с конфигурацией программы.')
