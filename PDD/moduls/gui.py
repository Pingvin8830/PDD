#!/bin/python3

from config    import settings as CONF
from dbmodels  import Answer
from dbmodels  import Question
from random    import randrange
from functions import write_image
from functions import write_log
from PIL       import Image
from PIL       import ImageTk
from sys       import argv
from tkinter   import Frame
from tkinter   import Label
from tkinter   import StringVar
from tkinter   import Tk
from widgets   import MyButton
from widgets   import MyEntry
from widgets   import MyLabel
from widgets   import MyMessage
from widgets   import MyRadio
from widgets   import MyText

def gui_exit ():
  window.destroy ()
  write_log ('Destroy window')

def main (type_gui = 'main'):
  global window
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
  write_log ('Start programm')
  write_log ('Result: BAD')
  window = Tk ()
  if   type_gui == 'main': app = MainMenu (window)
  elif type_gui == 'conf': app = Settings (window)
  window.title (CONF.get ('WINDOW', 'title'))
  window.geometry ('%dx%d+%d+%d' % (CONF.getint ('WINDOW', 'width'), CONF.getint ('WINDOW', 'height'), CONF.getint ('WINDOW', 'x_step'), CONF.getint ('WINDOW', 'y_step')))
  window.mainloop ()
  write_log ('Stop programm')
  write_log ('---------------------------------------------------------------------------------------', False)

class MyStaff (Frame):
  def __init__ (self, master, rw = 0, rs = 1, cl = 0, cs = 1, st = 'N'):
    super (MyStaff, self).__init__ (master)
    self.main_bttn = MyButton (self,         text = 'Главное меню', command = self.main_menu)
    self.help_bttn = MyButton (self, rw = 1, text = '   Помощь   ', command = self.help)
    self.exit_bttn = MyButton (self, rw = 2, text = '    Выход   ', command = gui_exit)
    self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

  def main_menu (self):
    write_log ('Switch main menu')
    self.master.destroy ()
    self.master = MainMenu (self.master.master)

  def help (self):
    write_log ('Switch help')
    self.master.destroy ()
    self.master = Help (self.master.master)

class QuestionForm (Frame):
  def __init__ (self, master):
    super (QuestionForm, self).__init__ (master)
    self.create_widgets ()
    
  def create_widgets (self):
    '''Создание виджетов'''
    self.answer = StringVar ()
    self.answer.set (None)
    self.title_lbl = MyLabel   (self, rw =  0, cs = 2)
    self.image_lbl = MyLabel (self, rw = 1, cs = 2, image = None)
    self.quest_msg = MyMessage (self, rw = 2, cs = 2, width = 800)
    self.dlm_1_lbl = MyLabel (self, rw = 3, cs = 2)
    self.ans_1_rad = MyRadio   (self, rw =  4,         st = 'W', variable = self.answer, value = '1')
    self.ans_1_msg = MyMessage (self, rw = 4, cl = 1, st = 'W', width = 800)
    self.ans_2_rad = MyRadio   (self, rw =  5,         st = 'W', variable = self.answer, value = '2')
    self.ans_2_msg = MyMessage (self, rw = 5, cl = 1, st = 'W', width = 800)
    self.ans_3_rad = MyRadio   (self, rw =  6,         st = 'W', variable = self.answer, value = '3')
    self.ans_3_msg = MyMessage (self, rw = 6, cl = 1, st = 'W', width = 800)
    self.ans_4_rad = MyRadio   (self, rw =  7,         st = 'W', variable = self.answer, value = '4')
    self.ans_4_msg = MyMessage (self, rw = 7, cl = 1, st = 'W', width = 800)
    self.ans_5_rad = MyRadio   (self, rw =  8,         st = 'W', variable = self.answer, value = '5')
    self.ans_5_msg = MyMessage (self, rw = 8, cl = 1, st = 'W', width = 800)
    self.dlm_2_lbl = MyLabel (self, rw = 9, cs = 2)
    self.dlm_3_lbl = MyLabel (self, rw = 12, cs = 2)
    self.next_bttn = MyButton  (self, rw = 13, cs = 2,           text = '    Далее   ')
    self.staff_frm = MyStaff   (self, rw = 14, cs = 2)

  def get_question (self):
    '''Задаёт вопрос'''
    self.ans_1_rad.grid_remove ()
    self.ans_1_msg.grid_remove ()
    self.ans_2_rad.grid_remove ()
    self.ans_2_msg.grid_remove ()
    self.ans_3_rad.grid_remove ()
    self.ans_3_msg.grid_remove ()
    self.ans_4_rad.grid_remove ()
    self.ans_4_msg.grid_remove ()
    self.ans_5_rad.grid_remove ()
    self.ans_5_msg.grid_remove ()
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
        if an ==1: self.ans_1_msg ['text'] = ao.text; self.ans_1_rad.grid (row = 4, sticky = 'W'); self.ans_1_msg.grid (row = 4, column = 1, sticky = 'W')
        elif an == 2: self.ans_2_msg ['text'] = ao.text; self.ans_2_rad.grid (row = 5, sticky = 'W'); self.ans_2_msg.grid (row = 5, column = 1, sticky = 'W')
        elif an == 3: self.ans_3_msg ['text'] = ao.text; self.ans_3_rad.grid (row = 6, sticky = 'W'); self.ans_3_msg.grid (row = 6, column = 1, sticky = 'W')
        elif an == 4: self.ans_4_msg ['text'] = ao.text; self.ans_4_rad.grid (row = 7, sticky = 'W'); self.ans_4_msg.grid (row = 7, column = 1, sticky = 'W')
        elif an == 5: self.ans_5_msg ['text'] = ao.text; self.ans_5_rad.grid (row = 8, sticky = 'W'); self.ans_5_msg.grid (row = 8, column = 1, sticky = 'W')
    self.title_lbl ['text'] = 'Билет № %d' % question.ticket
    self.quest_msg ['text'] = '%d. %s' % (question.number, question.text.replace ('\\', '\n'))
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
    self.ttl_1_lbl = MyLabel  (self,                 cs = 2, text = 'Тест на тему')
    self.ttl_2_lbl = MyLabel  (self, rw = 1,         cs = 2, text = CONF.get ('WINDOW', 'title'))
    self.delim_lbl = MyLabel  (self, rw = 2,         cs = 2)
    self.test_bttn = MyButton (self, rw = 3,                 text = '\nНачать тест\n', command = self.test)
    self.conf_bttn = MyButton (self, rw = 4,                 text = ' Настройки ',     command = self.settings)
    self.staff_frm = MyStaff  (self, rw = 3, rs = 2, cl = 1)

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
    self.title_lbl     = MyLabel  (self,          cs = 3,           text = CONF.CONF_FILE)
    self.font_sect_lbl = MyLabel  (self, rw =  1,         st = 'W', text = 'Шрифт')
    self.font_name_lbl = MyLabel  (self, rw =  2, cl = 1, st = 'W', text = 'Название')
    self.font_name_ent = MyEntry  (self, rw =  2, cl = 2, st = 'W', text = CONF.get ('FONT', 'name'))
    self.font_size_lbl = MyLabel  (self, rw =  3, cl = 1, st = 'W', text = 'Размер')
    self.font_size_ent = MyEntry  (self, rw =  3, cl = 2, st = 'W', text = CONF.getint ('FONT', 'size'))
    self.file_sect_lbl = MyLabel  (self, rw =  4,         st = 'W', text = 'Файлы')
    self.file_db___lbl = MyLabel  (self, rw =  5, cl = 1, st = 'W', text = 'БД')
    self.file_db___ent = MyEntry  (self, rw =  5, cl = 2, st = 'W', text = CONF.get ('FILES', 'db'))
    self.file_tmp__lbl = MyLabel  (self, rw =  6, cl = 1, st = 'W', text = 'Временный')
    self.file_tmp__ent = MyEntry  (self, rw =  6, cl = 2, st = 'W', text = CONF.get ('FILES', 'tmp'))
    self.file_log__lbl = MyLabel  (self, rw =  7, cl = 1, st = 'W', text = 'Лог')
    self.file_log__ent = MyEntry  (self, rw =  7, cl = 2, st = 'W', text = CONF.get ('FILES', 'log'))
    self.wind_sect_lbl = MyLabel  (self, rw =  8,         st = 'W', text = 'Окно')
    self.wind_ttl__lbl = MyLabel  (self, rw =  9, cl = 1, st = 'W', text = 'Заголовок')
    self.wind_ttl__ent = MyEntry  (self, rw =  9, cl = 2, st = 'W', text = CONF.get ('WINDOW', 'title'))
    self.wind_wdt__lbl = MyLabel  (self, rw = 10, cl = 1, st = 'W', text = 'Ширина')
    self.wind_wdt__ent = MyEntry  (self, rw = 10, cl = 2, st = 'W', text = CONF.getint ('WINDOW', 'width'))
    self.wind_hgt__lbl = MyLabel  (self, rw = 11, cl = 1, st = 'W', text = 'Высота')
    self.wind_hgt__ent = MyEntry  (self, rw = 11, cl = 2, st = 'W', text = CONF.getint ('WINDOW', 'height'))
    self.wind_xstp_lbl = MyLabel  (self, rw = 12, cl = 1, st = 'W', text = 'Левый край')
    self.wind_xstp_ent = MyEntry  (self, rw = 12, cl = 2, st = 'W', text = CONF.getint ('WINDOW', 'x_step'))
    self.wind_ystp_lbl = MyLabel  (self, rw = 13, cl = 1, st = 'W', text = 'Верхний край')
    self.wind_ystp_ent = MyEntry  (self, rw = 13, cl = 2, st = 'W', text = CONF.getint ('WINDOW', 'y_step'))
    self.tckt_sect_lbl = MyLabel  (self, rw = 14,         st = 'W', text = 'Билеты')
    self.tckt_cnt__lbl = MyLabel  (self, rw = 15, cl = 1, st = 'W', text = 'Количество')
    self.tckt_cnt__ent = MyEntry  (self, rw = 15, cl = 2, st = 'W', text = CONF.getint ('TICKET', 'count'))
    self.tckt_strt_lbl = MyLabel  (self, rw = 16, cl = 1, st = 'W', text = 'Начальный')
    self.tckt_strt_ent = MyEntry  (self, rw = 16, cl = 2, st = 'W', text = CONF.getint ('TICKET', 'start'))
    self.qstn_sect_lbl = MyLabel  (self, rw = 17,         st = 'W', text = 'Вопросы')
    self.qstn_cnt__lbl = MyLabel  (self, rw = 18, cl = 1, st = 'W', text = 'Количество')
    self.qstn_cnt__ent = MyEntry  (self, rw = 18, cl = 2, st = 'W', text = CONF.getint ('QUESTION', 'count'))
    self.qstn_strt_lbl = MyLabel  (self, rw = 19, cl = 1, st = 'W', text = 'Начальный')
    self.qstn_strt_ent = MyEntry  (self, rw = 19, cl = 2, st = 'W', text = CONF.getint ('QUESTION', 'start'))
    self.answ_sect_lbl = MyLabel  (self, rw = 20,         st = 'W', text = 'Ответы')
    self.answ_cnt__lbl = MyLabel  (self, rw = 21, cl = 1, st = 'W', text = 'Количество')
    self.answ_cnt__ent = MyEntry  (self, rw = 21, cl = 2, st = 'W', text = CONF.getint ('ANSWER', 'count'))
    self.answ_strt_lbl = MyLabel  (self, rw = 22, cl = 1, st = 'W', text = 'Начальный')
    self.answ_strt_ent = MyEntry  (self, rw = 22, cl = 2, st = 'W', text = CONF.getint ('ANSWER', 'start'))
    self.lgc__sect_lbl = MyLabel  (self, rw = 23,         st = 'W', text = 'Логика')
    self.lgc__err__lbl = MyLabel  (self, rw = 24, cl = 1, st = 'W', text = 'Количество ошибок')
    self.lgc__err__ent = MyEntry  (self, rw = 24, cl = 2, st = 'W', text = CONF.getint ('LOGIC', 'max_error'))
    self.lgc__type_lbl = MyLabel  (self, rw = 25, cl = 1, st = 'W', text = 'Логика теста')
    self.lgc__type_ent = MyEntry  (self, rw = 25, cl = 2, st = 'W', text = CONF.get    ('LOGIC', 'type_test'))
    self.lgc__tckt_lbl = MyLabel  (self, rw = 26, cl = 1, st = 'W', text = 'Номер билета')
    self.lgc__tckt_ent = MyEntry  (self, rw = 26, cl = 2, st = 'W', text = CONF.getint ('LOGIC', 'ticket'))
    self.delim_lbl     = MyLabel  (self, rw = 27, cs = 3)
    self.save_bttn     = MyButton (self, rw = 28, cs = 3,           text = '  Сохранить ', command = self.save)
    self.staff_frm     = MyStaff  (self, rw = 29, cs = 3)
        
  def save (self):
    '''Сохранение настроек'''
    write_log ('Switch save')
    CONF.set ('FONT',     'name',      self.font_name_ent.get ())
    CONF.set ('FONT',     'size',      self.font_size_ent.get ())
    CONF.set ('FILES',    'db',        self.file_db___ent.get ())
    CONF.set ('FILES',    'tmp',       self.file_tmp__ent.get ())
    CONF.set ('FILES',    'log',       self.file_log__ent.get ())
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
    CONF.set ('LOGIC',    'type_test', self.lgc__type_ent.get ())
    CONF.set ('LOGIC',    'ticket',    self.lgc__tckt_ent.get ())
    gui_exit ()
    main ('conf')

class Test (QuestionForm):
  '''Тестирование'''
  def __init__ (self, master):
    super (Test, self).__init__ (master)
    self.create_test ()
    write_log ('Create test menu')
    self.get_question   ()
    self.grid           ()

  def create_widgets (self):
    super (Test, self).create_widgets ()
    self.next_bttn ['command'] = self.save_answer

  def create_test (self):
    self.questions = [0]
    self.answers   = [0]
    self.errors    = [0]
    tn = None
    for question in range (CONF.getint ('QUESTION', 'count')):
      qn = question + CONF.getint ('QUESTION', 'start')
      if   CONF.get ('LOGIC', 'type_test') == 'random':        tn = randrange (CONF.getint ('TICKET', 'count')) + CONF.getint ('TICKET', 'start')
      elif CONF.get ('LOGIC', 'type_test') == 'ticket':        tn = CONF.getint ('LOGIC', 'ticket')
      elif CONF.get ('LOGIC', 'type_test') == 'random ticket':
        if not tn: tn = randrange (CONF.getint ('TICKET', 'count')) + CONF.getint ('TICKET', 'start')
      qo = Question (ticket = tn, number = qn)
      self.questions.append (qo)
      write_log ('Add  question with id %d in test' % qo.id)

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
    self.more_bttn = MyButton (self, rw = 3,         text = '\nПросмотр\n ошибок \n',  command = self.more)
    self.staff_frm = MyStaff  (self, rw = 3, cl = 1)

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

class More (QuestionForm):
  '''Подробные результаты'''
  def __init__ (self, master, answers, errors):
    super (More, self).__init__ (master)
    self.answers = answers
    self.errors  = errors
    self.number  = 0
    if self.errors [0]:
      self.number = 1
      self.get_question ()
    else:
      self.no_errors ()
    self.grid ()
    write_log ('Create more information menu')

  def no_errors (self):
    self.ans_1_rad.destroy ()
    self.ans_2_rad.destroy ()
    self.ans_3_rad.destroy ()
    self.ans_4_rad.destroy ()
    self.ans_5_rad.destroy ()
    self.ans_1_msg.destroy ()
    self.ans_2_msg.destroy ()
    self.ans_3_msg.destroy ()
    self.ans_4_msg.destroy ()
    self.ans_5_msg.destroy ()
    self.quest_msg.destroy ()
    self.image_lbl.destroy ()
    self.title_lbl ['text'] = 'Ошибок нет.'

  def create_widgets (self):
    super (More, self).create_widgets ()
    self.user_answer_lbl = MyLabel (self, rw = 10, cs = 2)
    self.good_answer_lbl = MyLabel (self, rw = 11, cs = 2)
    self.next_bttn ['command'] = self.done

  def get_question (self):
    self.ans_1_rad.grid_remove ()
    self.ans_1_msg.grid_remove ()
    self.ans_2_rad.grid_remove ()
    self.ans_2_msg.grid_remove ()
    self.ans_3_rad.grid_remove ()
    self.ans_3_msg.grid_remove ()
    self.ans_4_rad.grid_remove ()
    self.ans_4_msg.grid_remove ()
    self.ans_5_rad.grid_remove ()
    self.ans_5_msg.grid_remove ()
    question = self.errors [self.number]
    write_log ('Get  question with id %d' % question.id)
    good_answer = 0
    for answer in range (CONF.getint ('ANSWER', 'count')):
      an = answer + CONF.getint ('ANSWER', 'start')
      ao = Answer (ticket = question.ticket, question = question.number, number = an)
      write_log ('Add  answer   with id %d to question with id %d' % (ao.id, question.id))
      if ao.is_true:
        good_answer = an
        write_log ('It is true answer')
      if ao.text:
        if an == 1: self.ans_1_msg ['text'] = ao.text; self.ans_1_msg.grid (row = 4, column = 1, sticky = 'W')
        elif an == 2: self.ans_2_msg ['text'] = ao.text; self.ans_2_msg.grid (row = 5, column = 1, sticky = 'W')
        elif an == 3: self.ans_3_msg ['text'] = ao.text; self.ans_3_msg.grid (row = 6, column = 1, sticky = 'W')
        elif an == 4: self.ans_4_msg ['text'] = ao.text; self.ans_4_msg.grid (row = 7, column = 1, sticky = 'W')
        elif an == 5: self.ans_5_msg ['text'] = ao.text; self.ans_5_msg.grid (row = 8, column = 1, sticky = 'W')
    self.title_lbl ['text'] = 'Билет № %d' % question.ticket
    self.quest_msg ['text'] = '%d. %s' % (question.number, question.text.replace ('\\', '\n'))
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
    self.user_answer_lbl ['text'] = 'Ваш ответ:    %d' % self.answers [question.number]
    self.good_answer_lbl ['text'] = 'Верный ответ: %d' % good_answer
    
  def done (self):
    write_log ('Switch done')
    if self.number < len (self.errors) - 1:
      self.number += 1
      self.get_question ()
    else:
      write_log ('It was last question')
      self.destroy ()
      self = Result (self.master, self.answers, self.errors)
        
class Help (Frame):
  def __init__ (self, master):
    super (Help, self).__init__ (master)
    self.create_widgets ()
    self.grid ()

  def create_widgets (self):
    text  = 'Запуск:'
    text += '\n%s -c <CONF_FILE>\n' % argv [0]
    text += '\nCONF_FILE - файл конфигурации. Содержимое типа:\n'
    text += '\n[SECTION]'
    text += '\noption = <value>\n'
    text += '\nОписание настроек:'
    text += '\n[секция]   Параметр  Описание параметра                                        '
    text += '\n[FONT]     name      Название доступного шрифта                                '
    text += '\n[FONT]     size      Число - размер шрифта                                     '
    text += '\n[FILES]    db        Путь к файлу базы данных sqlite3 с тестом                 '
    text += '\n[FILES]    tmp       Путь к файлу для  сохранения изображений из БД            '
    text += '\n[FILES]    log       Путь к файлу для логирования работы Программы             '
    text += '\n[WINDOW]   title     Текст, отображаемый в заголовке окна                      '
    text += '\n[WINDOW]   width     Число - ширина окна в пискселях                           '
    text += '\n[WINDOW]   height    Число - высота окна в пикселях                            '
    text += '\n[WINDOW]   x_step    Число - отступ от левого края монитора в пикселях         '
    text += '\n[WINDOW]   y_step    Число - отступ от верхнего края монитора в пикселях       '
    text += '\n[TICKET]   count     Число - количество билетов для выборки                    '
    text += '\n[TICKET]   start     Число - смещение начала выборки билетов                   '
    text += '\n[QUESTION] count     Число - количество вопросов в одном билете                '
    text += '\n[QUESTION] start     Число - смещение начала выборки вопросов                  '
    text += '\n[ANSWER]   count     Число - максимальное количество ответов на один вопрос    '
    text += '\n[ANSWER]   start     Число - смещение начала выборки ответов                   '
    text += '\n[LOGIC]    max_error Число - количество ошибок, допустимое для сдачи теста     '
    text += '\n[LOGIC]    type_test random ticket - все вопросы из случайного билета          '
    text += '\n                     ticket        - все вопросы из конкретного билета         '
    text += '\n                     random        - вопросы выбираются по порядку из случайных'
    text += '\n                                     билетов                                   '
    text += '\n[LOGIC]    ticket    Число - номер билета при type_test = ticket\n             '
    self.title_lbl = MyLabel (self,         text = 'Программа проведения тестов')
    self.dlm_1_lbl = MyLabel (self, rw = 1)
    self.help__txt = MyText  (self, rw = 2, text = text)
    self.staff_frm = MyStaff (self, rw = 3)

if __name__ == '__main__':
  print ('Это всего-лишь модуль для работы с ГУИ.')
