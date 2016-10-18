#!/bin/python3

from os  import getcwd
from sys import path as PATH
PATH.append (getcwd () + '/moduls')

from config import settings as CONF
#from gui    import *

from   tkinter      import *
from   random       import randrange
from   PIL          import Image, ImageTk
from   datetime     import datetime
from   sys          import platform as OS
import sqlite3      as     lite

def set_var ():
  global CON
  global CUR
  try:
    CON = lite.connect (CONF.get ('FILES', 'db'))
    CUR = CON.cursor ()
  except:
    print ('Database not found!')
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

def gui_exit ():
  window.destroy ()
  write_log ('Destroy window')

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
  
def main (type_gui = 'main'):
  global window
  set_var ()
  write_log ('Start programm')
  write_log ('Result: BAD')
  window = Tk ()
  if   type_gui == 'main': app = MainMenu (window)
  elif type_gui == 'conf': app = Settings (window)
  window.title (CONF.get ('WINDOW', 'title'))
  window.geometry ('%dx%d+%d+%d' % (CONF.getint ('WINDOW', 'width'), CONF.getint ('WINDOW', 'height'), CONF.getint ('WINDOW', 'x_step'), CONF.getint ('WINDOW', 'y_step')))
  window.mainloop ()
  CON.close ()

class Question ():
  '''Вопросы'''
  def __init__ (self, ident = 0, ticket = 0, number = 0):
    if not ident:
      self.ticket     = int (ticket)
      self.number     = int (number)
      try:    self.id = CUR.execute ('SELECT id      FROM questions WHERE ticket = %d AND number = %d' % (self.ticket, self.number)).fetchone ()[0]
      except: self.id = CUR.execute ('SELECT max(id) FROM questions').fetchone () [0] + 1
    else:
      try:
        ident = int (ident)
        self.id     = CUR.execute ('SELECT id     FROM questions WHERE id = %d' % ident).fetchone () [0]
        self.ticket = CUR.execute ('SELECT ticket FROM questions WHERE id = %d' % self.id).fetchone () [0]
        self.number = CUR.execute ('SELECT number FROM questions WHERE id = %d' % self.id).fetchone () [0]
      except:
        print ('Do not find question with id %d in db.' % ident)
        self.id     = CUR.execute ('SELECT max(id) FROM questions').fetchone () [0] + 1
        self.ticket = 0
        self.number = 0
    try:    self.image  = CUR.execute ('SELECT image  FROM questions WHERE id = %d' % self.id).fetchone () [0]
    except: self.image  = None
    try:    self.text   = CUR.execute ('SELECT text   FROM questions WHERE id = %d' % self.id).fetchone () [0]
    except: self.text   = None
    write_log ('Init question with id %d' % self.id)

  def __str__ (self):
    if self.image: is_image = True
    else:          is_image = False
    return '''
id:        %d
ticket:    %d
number:    %d
is_image:  %s
text:      %s
is_db:     %s
''' % (self.id, self.ticket, self.number, is_image, self.text, str (self.is_db ()))

  def is_db (self):
    if CUR.execute ('SELECT * FROM questions WHERE id = %d' % self.id).fetchone ():
      return True
    else:
      return False

  def write (self):
    if self.is_db ():
      print ('Question now in db.')
      return
    CUR.execute ('INSERT INTO questions VALUES (?, ?, ?, ?, ?)', (self.id, self.ticket, self.number, self.text, self.image))
    CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Write question with id %d' % self.id)

  def update (self, field, value):
    if not self.is_db ():
      print ('Question not in db.')
      return
    CUR.execute ('UPDATE questions SET %s = "%s" WHERE id = %d' % (field, value, self.id))
    CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Update question with id %d' % self.id)

  def delete (self):
    if not self.is_db ():
      print ('Question not in db.')
      return
    CUR.execute ('DELETE FROM questions WHERE id = %d' % self.id)
    CON.commit ()
    write_log ('Delete question with id %d' % self.id)
    self.__init__ (ticket = self.ticket, number = self.number)

class Answer ():
  '''Варианты ответов'''
  def __init__ (self, ident = 0, ticket = 0, question = 0, number = 0):
    if ident:
      try:
        ident = int (ident)
        self.id       = CUR.execute ('SELECT id       FROM answers WHERE id = %d' % ident).fetchone () [0]
        self.ticket   = CUR.execute ('SELECT ticket   FROM answers WHERE id = %d' % self.id).fetchone () [0]
        self.question = CUR.execute ('SELECT question FROM answers WHERE id = %d' % self.id).fetchone () [0]
        self.number   = CUR.execute ('SELECT number   FROM answers WHERE id = %d' % self.id).fetchone () [0]
      except:
        print ('Do not find answer with id %d in db.' % ident)
        self.id       = CUR.execute ('SELECT max(id)  FROM answers').fetchone () [0] + 1
        self.ticket   = 0
        self.question = 0
        self.number   = 0
    else:
      self.ticket        = int (ticket)
      self.question      = int (question)
      self.number        = int (number)
      try:    self.id    = CUR.execute ('SELECT id      FROM answers WHERE ticket = %d AND question = %d AND number = %d' % (self.ticket, self.question, self.number)).fetchone () [0]
      except: self.id    = CUR.execute ('SELECT max(id) FROM answers').fetchone () [0] + 1
    try:
      self.text    = CUR.execute ('SELECT text    FROM answers WHERE id = %d' % self.id).fetchone () [0]
      while len (self.text) < 68:
        self.text = self.text + ' '
    except: self.text    = None
    try:    self.is_true = CUR.execute ('SELECT is_true FROM answers WHERE id = %d' % self.id).fetchone () [0]
    except: self.is_true = 0
    write_log ('Init answer   with id %d' % self.id)
    
  def __str__ (self):
    return '''
id:       %d
ticket:   %d
question: %d
number:   %d
is_true:  %s
text:     %s
is_db:    %s
''' % (self.id, self.ticket, self.question, self.number, str (self.is_true), self.text, str (self.is_db ()))

  def is_db (self):
    if CUR.execute ('SELECT * FROM answers WHERE id = %d' % self.id).fetchone ():
      return True
    else:
      return False

  def write (self):
    if self.is_db ():
      print ('Answer now in db.')
      return
    CUR.execute ('INSERT INTO answers VALUES (?, ?, ?, ?, ?, ?)', (self.id, self.ticket, self.question, self.number, self.is_true, self.text))
    CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Write answer with id %d' % self.id)

  def update (self, field, value):
    if not self.is_db ():
      print ('Answer not in db.')
      return
    CUR.execute ('UPDATE answers SET %s = "%s" WHERE id = %d' % (field, value, self.id))
    CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Update answer with id %d' % self.id)

  def delete (self):
    if not self.is_db ():
      print ('Answer now in db.')
      return
    CUR.execute ('DELETE FROM answers WHERE id = %d' % self.id)
    CON.commit ()
    write_log ('Delete answer with id %d' % self.id)
    self.__init__ (ticket = self.ticket, question = self.question, number = self.number)

class MyRadio (Radiobutton):
  '''Радиокнопки'''
  def __init__ (self, master, value, variable, text = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N, command = None):
    super (MyRadio, self).__init__ (master, text = text, command = command, value = value, variable = variable, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')))
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
        
class MyMessage (Message):
  '''Метки'''
  def __init__ (self, master, text = None, image = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N, width = None, height = None):
    super (MyMessage, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), width = width, height = height)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyButton (Button):
  '''Кнопки'''
  def __init__ (self, master, text, command = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N):
    super (MyButton, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), command = command)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyLabel (Label):
  def __init__ (self, master, text = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N):
    super (MyLabel, self).__init__ (master, text = text, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')))
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyEntry (Entry):
  def __init__ (self, master, text = '', rw = 0, rs = 1, cl = 0, cs = 1, st = N, width = 40):
    super (MyEntry, self).__init__ (master, font = (CONF.get ('FONT', 'name'), CONF.get ('FONT', 'size')), width = width)
    self.insert (0, text)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
        
class MainMenu (Frame):
  '''Главное меню'''
  def __init__ (self, master):
    '''Инициализирует рамку GUI'''
    super (MainMenu, self).__init__ (master)
    self.create_widgets ()
    self.grid           ()
    write_log ('Create main menu')

  def create_widgets (self):
    '''Создание виджетов'''
    self.ttl_1_lbl = MyLabel   (self,                 cs = 3, text = 'Тест на знания')
    self.ttl_2_lbl = MyLabel   (self, rw = 1,         cs = 3, text = 'Правил Дорожного Движения')
    self.delim_lbl = MyMessage (self, rw = 2,         cs = 3)
    self.test_bttn = MyButton  (self, rw = 3,                 text = 'Начать тест', command = self.test)
    self.conf_bttn = MyButton  (self, rw = 3, cl = 1,         text = ' Настройки ', command = self.settings)
    self.exit_bttn = MyButton  (self, rw = 3, cl = 2,         text = '   Выход   ', command = gui_exit)

  def test (self):
    '''Тест'''
    write_log ('Switch start test')
    self.destroy ()
    self = Test (self.master)

  def settings (self):
    '''Настройки'''
    write_log ('Switch settings')
    self.destroy ()
    self = Settings (self.master)

class Settings (Frame):
  '''Настройки'''
  def __init__ (self, master):
    super (Settings, self).__init__ (master)
    self.create_widgets ()
    self.grid ()
    write_log ('Create settings menu')

  def create_widgets (self):
    '''Создание виджетов'''
    self.title_lbl     = MyLabel  (self,          cs = 3,         text = 'Настройки программы')
    self.font_sect_lbl = MyLabel  (self, rw =  1,         st = W, text = 'Шрифт')
    self.font_name_lbl = MyLabel  (self, rw =  2, cl = 1, st = W, text = 'Название')
    self.font_name_ent = MyEntry  (self, rw =  2, cl = 2, st = W, text = CONF.get ('FONT', 'name'))
    self.font_size_lbl = MyLabel  (self, rw =  3, cl = 1, st = W, text = 'Размер')
    self.font_size_ent = MyEntry  (self, rw =  3, cl = 2, st = W, text = CONF.getint ('FONT', 'size'))
    self.db___sect_lbl = MyLabel  (self, rw =  4,         st = W, text = 'БД')
    self.db___path_lbl = MyLabel  (self, rw =  5, cl = 1, st = W, text = 'Путь')
    self.db___path_ent = MyEntry  (self, rw =  5, cl = 2, st = W, text = CONF.get ('FILES', 'db'))
    self.db___name_lbl = MyLabel  (self, rw =  6, cl = 1, st = W, text = 'Имя')
    self.db___name_ent = MyEntry  (self, rw =  6, cl = 2, st = W, text = CONF.get ('FILES', 'db'))
    self.temp_sect_lbl = MyLabel  (self, rw =  7,         st = W, text = 'Временное')
    self.temp_path_lbl = MyLabel  (self, rw =  8, cl = 1, st = W, text = 'Путь')
    self.temp_path_ent = MyEntry  (self, rw =  8, cl = 2, st = W, text = CONF.get ('FILES', 'tmp'))
    self.temp_img__lbl = MyLabel  (self, rw =  9, cl = 1, st = W, text = 'Изображение')
    self.temp_img__ent = MyEntry  (self, rw =  9, cl = 2, st = W, text = CONF.get ('FILES', 'tmp'))
    self.log__sect_lbl = MyLabel  (self, rw = 10,         st = W, text = 'Лог-файл')
    self.log__path_lbl = MyLabel  (self, rw = 11, cl = 1, st = W, text = 'Путь')
    self.log__path_ent = MyEntry  (self, rw = 11, cl = 2, st = W, text = CONF.get ('FILES', 'log'))
    self.log__name_lbl = MyLabel  (self, rw = 12, cl = 1, st = W, text = 'Имя файла')
    self.log__name_ent = MyEntry  (self, rw = 12, cl = 2, st = W, text = CONF.get ('FILES', 'log'))
    self.wind_sect_lbl = MyLabel  (self, rw = 13,         st = W, text = 'Окно')
    self.wind_ttl__lbl = MyLabel  (self, rw = 14, cl = 1, st = W, text = 'Заголовок')
    self.wind_ttl__ent = MyEntry  (self, rw = 14, cl = 2, st = W, text = CONF.get ('WINDOW', 'title'))
    self.wind_wdt__lbl = MyLabel  (self, rw = 15, cl = 1, st = W, text = 'Ширина')
    self.wind_wdt__ent = MyEntry  (self, rw = 15, cl = 2, st = W, text = CONF.getint ('WINDOW', 'width'))
    self.wind_hgt__lbl = MyLabel  (self, rw = 16, cl = 1, st = W, text = 'Высота')
    self.wind_hgt__ent = MyEntry  (self, rw = 16, cl = 2, st = W, text = CONF.getint ('WINDOW', 'height'))
    self.wind_xstp_lbl = MyLabel  (self, rw = 17, cl = 1, st = W, text = 'Левый край')
    self.wind_xstp_ent = MyEntry  (self, rw = 17, cl = 2, st = W, text = CONF.getint ('WINDOW', 'x_step'))
    self.wind_ystp_lbl = MyLabel  (self, rw = 18, cl = 1, st = W, text = 'Верхний край')
    self.wind_ystp_ent = MyEntry  (self, rw = 18, cl = 2, st = W, text = CONF.getint ('WINDOW', 'y_step'))
    self.tckt_sect_lbl = MyLabel  (self, rw = 19,         st = W, text = 'Билеты')
    self.tckt_cnt__lbl = MyLabel  (self, rw = 20, cl = 1, st = W, text = 'Количество')
    self.tckt_cnt__ent = MyEntry  (self, rw = 20, cl = 2, st = W, text = CONF.getint ('TICKET', 'count'))
    self.tckt_strt_lbl = MyLabel  (self, rw = 21, cl = 1, st = W, text = 'Начальный')
    self.tckt_strt_ent = MyEntry  (self, rw = 21, cl = 2, st = W, text = CONF.getint ('TICKET', 'start'))
    self.qstn_sect_lbl = MyLabel  (self, rw = 22,         st = W, text = 'Вопросы')
    self.qstn_cnt__lbl = MyLabel  (self, rw = 23, cl = 1, st = W, text = 'Количество')
    self.qstn_cnt__ent = MyEntry  (self, rw = 23, cl = 2, st = W, text = CONF.getint ('QUESTION', 'count'))
    self.qstn_strt_lbl = MyLabel  (self, rw = 24, cl = 1, st = W, text = 'Начальный')
    self.qstn_strt_ent = MyEntry  (self, rw = 24, cl = 2, st = W, text = CONF.getint ('QUESTION', 'start'))
    self.answ_sect_lbl = MyLabel  (self, rw = 25,         st = W, text = 'Ответы')
    self.answ_cnt__lbl = MyLabel  (self, rw = 26, cl = 1, st = W, text = 'Количество')
    self.answ_cnt__ent = MyEntry  (self, rw = 26, cl = 2, st = W, text = CONF.getint ('ANSWER', 'count'))
    self.answ_strt_lbl = MyLabel  (self, rw = 27, cl = 1, st = W, text = 'Начальный')
    self.answ_strt_ent = MyEntry  (self, rw = 27, cl = 2, st = W, text = CONF.getint ('ANSWER', 'start'))
    self.lgc__sect_lbl = MyLabel  (self, rw = 28,         st = W, text = 'Логика')
    self.lgc__err__lbl = MyLabel  (self, rw = 29, cl = 1, st = W, text = 'Количество ошибок')
    self.lgc__err__ent = MyEntry  (self, rw = 29, cl = 2, st = W, text = CONF.getint ('LOGIC', 'max_error'))
    self.delim_lbl     = MyLabel  (self, rw = 30, cs = 3)
    self.save_bttn     = MyButton (self, rw = 31,         st = E, text = '  Сохранить ', command = self.save)
    self.main_bttn     = MyButton (self, rw = 31, cl = 1, st = N, text = 'Главное меню', command = self.main_menu)
    self.exit_bttn     = MyButton (self, rw = 31, cl = 2, st = W, text = '    Выход   ', command = gui_exit)
        
  def save (self):
    '''Сохранение настроек'''
    write_log ('Switch save')
    CONF.set ('FONT',     'name',      self.font_name_ent.get ())
    CONF.set ('FONT',     'size',      self.font_size_ent.get ())
    CONF.set ('FILES',    'db',        self.db___path_ent.get ())
    CONF.set ('FILES',    'tmp',       self.temp_path_ent.get ())
    CONF.set ('FILES',    'log',       self.log__path_ent.get ())
    CONF.set ('WINDOW',   'title',     self.wind_ttl__ent.get ())
    CONF.set ('WINDOW',   'width',     self.wind_wdt__ent.get ())
    CONF.set ('WINDOW',   'height',    self.wind_hgt__ent.get ())
    CONF.set ('WINDOW',   'x_step',    self.wind_xstp_ent.get ())
    CONF.set ('WINDOW',   'y_step',    self.wind_ystp_ent.get ())
    CONF.set ('TICKET',   'count',     self.tckt_cnt__ent.get ())
    CONF.set ('TICKET',   'start',     self.tckt_strt_ent.get ())
    CONF.set ('QUESTION', 'count',     self.qstn_cnt__ent.get ())
    CONF.set ('QUESTION', 'start',     self.qstn_strt_ent.get ())
    CONF.set ('ANSWER',   'count',     self.answ_cnt__ent.get ())
    CONF.set ('ANSWER',   'start',     self.answ_strt_ent.get ())
    CONF.set ('LOGIC',    'max_error', self.lgc__err__ent.get ())
    gui_exit ()
    main ('conf')

  def main_menu (self):
    write_log ('Switch main menu')
    self.destroy ()
    self = MainMenu (self.master)
            
class Test (Frame):
  '''Тестирование'''
  def __init__ (self, master):
    super (Test, self).__init__ (master)
    self.questions = [0]
    for question in range (CONF.getint ('QUESTION', 'count')):
      qn = question + CONF.getint ('QUESTION', 'start')
      qo = Question (ticket = randrange (CONF.getint ('TICKET', 'count')) + CONF.getint ('TICKET', 'start'), number = qn)
      self.questions.append (qo)
      write_log ('Add  question with id %d in test' % qo.id)
    self.answers  = [0]
    self.errors   = [0]
    self.create_widgets ()
    write_log ('Create test menu')
    self.get_question   ()
    self.grid           ()

  def create_widgets (self):
    '''Создание виджетов'''
    self.answer = StringVar ()
    self.answer.set (None)
    self.title_lbl = MyLabel   (self, rw =  0, cs = 2)
    self.image_lbl = MyMessage (self, rw =  1, cs = 2,         image = None)
    self.quest_lbl = MyMessage (self, rw =  2, cs = 2,         width = 800)
    self.dlm_1_lbl = MyMessage (self, rw =  3, cs = 2)
    self.ans_1_rad = MyRadio   (self, rw =  4,         st = W, variable = self.answer, value = '1')
    self.ans_1_lbl = MyMessage (self, rw =  4, cl = 1, st = W, width = 800)
    self.ans_2_rad = MyRadio   (self, rw =  5,         st = W, variable = self.answer, value = '2')
    self.ans_2_lbl = MyMessage (self, rw =  5, cl = 1, st = W, width = 800)
    self.ans_3_rad = MyRadio   (self, rw =  6,         st = W, variable = self.answer, value = '3')
    self.ans_3_lbl = MyMessage (self, rw =  6, cl = 1, st = W, width = 800)
    self.ans_4_rad = MyRadio   (self, rw =  7,         st = W, variable = self.answer, value = '4')
    self.ans_4_lbl = MyMessage (self, rw =  7, cl = 1, st = W, width = 800)
    self.ans_5_rad = MyRadio   (self, rw =  8,         st = W, variable = self.answer, value = '5')
    self.ans_5_lbl = MyMessage (self, rw =  8, cl = 1, st = W, width = 800)
    self.dlm_2_lbl = MyMessage (self, rw =  9, cs = 2)
    self.next_bttn = MyButton  (self, rw = 10, cs = 2, st = S, text = '    Далее   ', command = self.save_answer)
    self.canc_bttn = MyButton  (self, rw = 11, cs = 2, st = S, text = 'Главное меню', command = self.main_menu)
    self.exit_bttn = MyButton  (self, rw = 12, cs = 2, st = S, text = '    Выход   ', command = gui_exit)

  def get_question (self):
    '''Задаёт вопрос'''
    self.ans_1_rad.grid_remove ()
    self.ans_1_lbl.grid_remove ()
    self.ans_2_rad.grid_remove ()
    self.ans_2_lbl.grid_remove ()
    self.ans_3_rad.grid_remove ()
    self.ans_3_lbl.grid_remove ()
    self.ans_4_rad.grid_remove ()
    self.ans_4_lbl.grid_remove ()
    self.ans_5_rad.grid_remove ()
    self.ans_5_lbl.grid_remove ()
    question = self.questions [len (self.answers)]
    write_log ('Get  question with id %d' % question.id)
    self.good_answer = 0
    for answer in range (CONF.getint ('ANSWER', 'count')):
      an = answer + CONF.getint ('ANSWER', 'start')
      ao = Answer (ticket = question.ticket, question = question.number, number = an)
      write_log ('Add  answer   with id %d to question with id %d' % (ao.id, question.id))
      if ao.is_true:
        self.good_answer = an
        write_log ('It is true answer')
      if ao.text:
        if   an == 1: self.ans_1_lbl ['text'] = ao.text; self.ans_1_rad.grid (row = 4, sticky = W); self.ans_1_lbl.grid (row = 4, column = 1, sticky = W)
        elif an == 2: self.ans_2_lbl ['text'] = ao.text; self.ans_2_rad.grid (row = 5, sticky = W); self.ans_2_lbl.grid (row = 5, column = 1, sticky = W)
        elif an == 3: self.ans_3_lbl ['text'] = ao.text; self.ans_3_rad.grid (row = 6, sticky = W); self.ans_3_lbl.grid (row = 6, column = 1, sticky = W)
        elif an == 4: self.ans_4_lbl ['text'] = ao.text; self.ans_4_rad.grid (row = 7, sticky = W); self.ans_4_lbl.grid (row = 7, column = 1, sticky = W)
        elif an == 5: self.ans_5_lbl ['text'] = ao.text; self.ans_5_rad.grid (row = 8, sticky = W); self.ans_5_lbl.grid (row = 8, column = 1, sticky = W)
    self.title_lbl ['text'] = 'Билет № %d' % question.ticket
    self.quest_lbl ['text'] = '%d. %s'     % (question.number, question.text.replace ('\\', '\n'))
    self.image_lbl.destroy ()
    try:
      write_image (question.image)
      self.image = Image.open (CONF.get ('FILES', 'tmp'))
      img = ImageTk.PhotoImage (self.image)
      self.image.close ()
      self.image = img
    except:
      self.image = None
    self.image_lbl = Label (self, image = self.image)
    self.image_lbl.grid (row = 1, columnspan = 2)
    self.answer.set (None)
        
  def save_answer (self):
    '''Сохранение ответа'''
    write_log ('Switch done')
    if self.answer.get () == 'None': return
    self.answers [0] += 1
    self.answers.append (int (self.answer.get ()))
    write_log ('User answer: %s' % self.answer.get ())
    write_log ('Good answer: %d' % self.good_answer)
    if int (self.answer.get ()) != self.good_answer:
      self.errors [0] += 1
      self.errors.append (self.questions [self.answers [0]])
      write_log ('Add error answer to question with id %d' % self.questions [self.answers [0]].id)
    if self.answers [0] < CONF.getint ('QUESTION', 'count'):
      self.get_question ()
    else:
      write_log ('It was last question')
      self.destroy ()
      self = Result (self.master, self.answers, self.errors)
        
  def main_menu (self):
    '''Выход в главное меню'''
    write_log ('Switch main menu')
    self.destroy ()
    self = MainMenu (self.master)

class Result (Frame):
  '''Результаты'''
  def __init__ (self, master, answers, errors):
    super (Result, self).__init__ (master)
    self.answers = answers
    self.errors  = errors
    self.create_widgets ()
    self.grid ()
    write_log ('Create result menu')

  def result (self):
    '''Подводит итоги'''
    write_log ('Count errors: %d' % self.errors [0])
    write_log ('Max errors: %d' % CONF.getint ('LOGIC', 'max_error'))
    if self.errors [0] <= CONF.getint ('LOGIC', 'max_error'):
      write_log ('Result: OK')
      return 'Экзамен сдан'
    else:
      write_log ('Result: BAD')
      return 'Переэкзаменовка'

  def create_widgets (self):
    '''Создание виджетов'''
    self.title_lbl = MyLabel  (self,         cs = 2, text = 'Результаты')
    self.resul_lbl = MyLabel  (self, rw = 1, cs = 2, text = self.result ())
    self.delim_lbl = MyLabel  (self, rw = 2, cs = 2)
    self.more_bttn = MyButton (self, rw = 3, cs = 2, text = '      Просмотр ошибок     ',  command = self.more)
    self.main_bttn = MyButton (self, rw = 4,         text = 'Главное меню',     command = self.main_menu)
    self.exit_bttn = MyButton (self, rw = 4, cl = 1, text = '    Выход   ',     command = gui_exit)

  def more (self):
    '''Вывод подробностей'''
    write_log ('Switch more information')
    self.destroy ()
    self = More (self.master, self.answers, self.errors)

  def main_menu (self):
    '''Выход в главное меню'''
    write_log ('Switch main menu')
    self.destroy ()
    self = MainMenu (self.master)

class More (Frame):
  '''Подробные результаты'''
  def __init__ (self, master, answers, errors):
    super (More, self).__init__ (master)
    self.answers = answers
    self.errors  = errors
    self.create_widgets ()
    self.grid ()
    write_log ('Create more information menu')

  def create_widgets (self):
    '''Создание виджетов'''
    mes = '      Ошибки при прохождении теста      \n\n'
    mes += 'Количество ошибок:                 %d  \n\n' % self.errors [0]
    mes += '+-----+------+---------+------------+ \n'
    mes += '|Билет|Вопрос|Ваш ответ|Верный ответ| \n'
    mes += '+-----+------+---------+------------+ \n'
    for question in self.errors [1:]:
      ticket = str (question.ticket)
      number = str (question.number)
      if question.ticket < 10: ticket = ' ' + ticket
      if question.number < 10: number = ' ' + number
      for answer in range (CONF.getint ('ANSWER', 'count')):
        good_answer = answer + 1
        ao = Answer (ticket = question.ticket, question = question.number, number = good_answer)
        if ao.is_true: break
      mes += '|   %s|    %s|        %d|           %d| \n' % (ticket, number, self.answers [question.number], good_answer)
    mes += '+-----+------+---------+------------+ \n\n'
    self.table_mes = MyMessage (self,         cs = 2, text = mes)
    self.main_bttn = MyButton  (self, rw = 1,         text = 'Главное меню', command = self.main_menu)
    self.exit_bttn = MyButton  (self, rw = 1, cl = 1, text = '    Выход   ', command = gui_exit)

  def main_menu (self):
    '''Выход в главное меню'''
    write_log ('Switch main menu')
    self.destroy ()
    self = MainMenu (self.master)

main ()
write_log ('Stop programm')
write_log ('---------------------------------------------------------------------------------------', False)
