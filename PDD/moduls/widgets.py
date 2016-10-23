#!/bin/python3

from config  import settings as CONF
from tkinter import Button
from tkinter import Entry
from tkinter import END
from tkinter import Frame
from tkinter import Label
from tkinter import Message
from tkinter import Radiobutton
from tkinter import Scrollbar
from tkinter import Text

class MyText (Text):
  def __init__ (self, master, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N', text = None, wrap = 'word', width = 80, height = 30):
    '''Поле для ввода текста'''
    super (MyText, self).__init__ (master, wrap = wrap, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), width = width, height = height)
    if text: self.insert (0.0, text)
    self ['state'] = 'disabled'
    self.scr = Scrollbar (master, command = self.yview)
    self.configure (yscrollcommand = self.scr.set)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
    self.scr.grid (row = rw, rowspan = 1, column = cl + 1, columnspan = 1, sticky = 'E')

  def update_text (self, text):
    self ['state'] = 'normal'
    self.delete (0.0, END)
    self.insert (0.0, text)
    self ['state'] = 'disabled'

class MyRadio (Radiobutton):
  '''Радиокнопки'''
  def __init__ (self, master, value, variable, text = None, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N', command = None):
    super (MyRadio, self).__init__ (master, text = text, command = command, value = value, variable = variable, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')))
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
        
class MyMessage (Message):
  '''Метки'''
  def __init__ (self, master, text = None, image = None, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N', width = None, height = None, justify = 'left'):
    super (MyMessage, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), width = width, height = height, justify = justify)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyButton (Button):
  '''Кнопки'''
  def __init__ (self, master, text, command = None, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N'):
    super (MyButton, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), command = command)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyLabel (Label):
<<<<<<< HEAD
  def __init__ (self, master, text = None, image = None, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N'):
    super (MyLabel, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')))
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyEntry (Entry):
  def __init__ (self, master, text = '', rw = 0, rs = 1, cl = 0, cs = 1, st = 'N', width = 40):
    super (MyEntry, self).__init__ (master, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), width = width)
    self.insert (0, text)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

if __name__ == '__main__':
  print ('Это всего-лишь модуль, содержащий виджеты.')
