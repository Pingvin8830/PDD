#!/bin/python3

from   tkinter      import *
from   random       import randrange
from   PIL          import Image, ImageTk
from   configparser import RawConfigParser
import sqlite3      as     lite

conf = RawConfigParser ()
try:
    conf.read ('W:/Общая/VAA/python/my_progs/PDD/PDD.conf')
    CONF = 'W:/Общая/VAA/python/my_progs/PDD/PDD.conf'
except:
    conf.read ('/data/shells/python/configs/PDD.conf')
    CONF = '/data/shells/python/configs/PDD.conf'

def set_var ():
    global FONT
    global CON
    global CUR
    global IMAGE
    global SIZE
    FONT  = (conf.get ('FONT', 'name'), conf.getint ('FONT', 'size'))
    try:
        CON   = lite.connect ('%s/%s' % (conf.get ('DATABASE', 'path'), conf.get ('DATABASE', 'name')))
        CUR   = CON.cursor ()
    except:
        print ('Database not found!')
    IMAGE = '%s/%s' % (conf.get ('TMP', 'path'), conf.get ('TMP', 'image'))
    SIZE  = '%dx%d+%d+%d' % (conf.getint ('WINDOW', 'width'), conf.getint ('WINDOW', 'height'), conf.getint ('WINDOW', 'x_step'), conf.getint ('WINDOW', 'y_step'))

def gui_exit ():
    window.destroy ()

def write_image (data):
    file = open (IMAGE, 'wb')
    file.write (data)
    file.close ()

def main (type_gui = 'main'):
    global window
    set_var ()
    window = Tk ()
    if   type_gui == 'main': app = MainMenu (window)
    elif type_gui == 'conf': app = Settings (window)
    window.title (conf.get ('WINDOW', 'title'))
    window.geometry (SIZE)
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
                self.id     = CUR.execute ('SELECT id     FROM questions WHERE id = %d' % ident).fetchone () [0]
                self.ticket = CUR.execute ('SELECT ticket FROM questions WHERE id = %d' % self.id).fetchone () [0]
                self.number = CUR.execute ('SELECT number FROM questions WHERE id = %d' % self.id).fetchone () [0]
            except:
                self.id     = CUR.execute ('SELECT max(id) FROM questions').fetchone () [0] + 1
                self.ticket = 0
                self.number = 0
        try:    self.image  = CUR.execute ('SELECT image  FROM questions WHERE id = %d' % self.id).fetchone () [0]
        except: self.image  = None
        try:    self.text   = CUR.execute ('SELECT text   FROM questions WHERE id = %d' % self.id).fetchone () [0]
        except: self.text   = None

    def __str__ (self):
        if self.image: is_image = True
        else:          is_image = False
        return '''
id:       %d
ticket:   %d
number:   %d
is_image: %s
text:     %s
is_db:    %s
''' % (self.id, self.ticket, self.number, is_image, self.text, str (self.is_db ()))

    def is_db (self):
        if CUR.execute ('SELECT * FROM questions WHERE id = %d' % self.id).fetchone ():
            return True
        else:
            return False

    def write (self):
        if self.is_db ():
            return
        CUR.execute ('INSERT INTO questions VALUES (?, ?, ?, ?, ?)', (self.id, self.ticket, self.number, self.text, self.image))
        CON.commit ()
        self.__init__ (ident = self.id)

    def update (self, field, value):
        if not self.is_db ():
            return
        CUR.execute ('UPDATE questions SET %s = "%s" WHERE id = %d' % (field, value, self.id))
        CON.commit ()
        self.__init__ (ident = self.id)

class Answer ():
    '''Варианты ответов'''
    def __init__ (self, ident = 0, ticket = 0, question = 0, number = 0):
        if ident:
            try:
                self.id       = CUR.execute ('SELECT id       FROM answers WHERE id = %d' % ident).fetchone () [0]
                self.ticket   = CUR.execute ('SELECT ticket   FROM answers WHERE id = %d' % self.id).fetchone () [0]
                self.question = CUR.execute ('SELECT question FROM answers WHERE id = %d' % self.id).fetchone () [0]
                self.number   = CUR.execute ('SELECT number   FROM answers WHERE id = %d' % self.id).fetchone () [0]
            except:
                self.id       = CUR.execute ('SELECT max(id)  FROM answers').fetchone () [0] + 1
                self.ticket   = 0
                self.question = 0
                self.number   = 0
        else:
            self.ticket       = int (ticket)
            self.question     = int (question)
            self.number       = int (number)
            try:    self.id   = CUR.execute ('SELECT id      FROM answers WHERE ticket = %d AND question = %d AND number = %d' % (self.ticket, self.question, self.number)).fetchone () [0]
            except: self.id   = CUR.execute ('SELECT max(id) FROM answers').fetchone () [0] + 1
        try:
            self.text     = CUR.execute ('SELECT text    FROM answers WHERE id = %d' % self.id).fetchone () [0]
            while len (self.text) < 68:
                self.text = self.text + ' '
        except: self.text     = ''
        try:    self.is_true  = CUR.execute ('SELECT is_true FROM answers WHERE id = %d' % self.id).fetchone () [0]
        except: self.is_true  = False

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
            return
        CUR.execute ('INSERT INTO answers VALUES (?, ?, ?, ?, ?, ?)', (self.id, self.ticket, self.question, self.number, self.is_true, self.text))
        CON.commit ()
        self.__init__ (ident = self.id)

    def update (self, field, value):
        if not self.is_db ():
            return
        CUR.execute ('UPDATE answers SET %s = "%s" WHERE id = %d' % (field, value, self.id))
        CON.commit ()
        self.__init__ (ident = self.id)
        
class MyRadio (Radiobutton):
    '''Радиокнопки'''
    def __init__ (self, master, value, variable, text = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N, command = None):
        super (MyRadio, self).__init__ (master, text = text, command = command, value = value, variable = variable, font = FONT)
        self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
        
class MyMessage (Message):
    '''Метки'''
    def __init__ (self, master, text = None, image = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N, width = None, height = None):
        super (MyMessage, self).__init__ (master, text = text, font = FONT, width = width, height = height)
        self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyButton (Button):
    '''Кнопки'''
    def __init__ (self, master, text, command = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N):
        super (MyButton, self).__init__ (master, text = text, font = FONT, command = command)
        self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyLabel (Label):
    def __init__ (self, master, text = None, rw = 0, rs = 1, cl = 0, cs = 1, st = N):
        super (MyLabel, self).__init__ (master, text = text, font = FONT)
        self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)

class MyEntry (Entry):
    def __init__ (self, master, text = '', rw = 0, rs = 1, cl = 0, cs = 1, st = N, width = 40):
        super (MyEntry, self).__init__ (master, font = FONT, width = width)
        self.insert (0, text)
        self.grid (row = rw, rowspan = rs, column = cl, columnspan = cs, sticky = st)
        
class MainMenu (Frame):
    '''Главное меню'''
    def __init__ (self, master):
        '''Инициализирует рамку GUI'''
        super (MainMenu, self).__init__ (master)
        self.create_widgets ()
        self.grid           ()

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
        self.destroy ()
        self = Test (self.master)

    def settings (self):
        '''Настройки'''
        self.destroy ()
        self = Settings (self.master)

class Settings (Frame):
    '''Настройки'''
    def __init__ (self, master):
        super (Settings, self).__init__ (master)
        self.create_widgets ()
        self.grid ()

    def create_widgets (self):
        '''Создание виджетов'''
        self.title_lbl     = MyLabel  (self,                  cs = 3,         text = 'Настройки программы')
        self.font_sect_lbl = MyLabel  (self, rw =  1,                 st = W, text = 'Шрифт')
        self.font_name_lbl = MyLabel  (self, rw =  2, cl = 1,         st = W, text = 'Название')
        self.font_name_ent = MyEntry  (self, rw =  2, cl = 2,         st = W, text = conf.get ('FONT', 'name'))
        self.font_size_lbl = MyLabel  (self, rw =  3, cl = 1,         st = W, text = 'Размер')
        self.font_size_ent = MyEntry  (self, rw =  3, cl = 2,         st = W, text = conf.get ('FONT', 'size'))
        self.db___sect_lbl = MyLabel  (self, rw =  4,                 st = W, text = 'БД')
        self.db___path_lbl = MyLabel  (self, rw =  5, cl = 1,         st = W, text = 'Путь')
        self.db___path_ent = MyEntry  (self, rw =  5, cl = 2,         st = W, text = conf.get ('DATABASE', 'path'))
        self.db___name_lbl = MyLabel  (self, rw =  6, cl = 1,         st = W, text = 'Имя')
        self.db___name_ent = MyEntry  (self, rw =  6, cl = 2,         st = W, text = conf.get ('DATABASE', 'name'))
        self.temp_sect_lbl = MyLabel  (self, rw =  7,                 st = W, text = 'Временное')
        self.temp_path_lbl = MyLabel  (self, rw =  8, cl = 1,         st = W, text = 'Путь')
        self.temp_path_ent = MyEntry  (self, rw =  8, cl = 2,         st = W, text = conf.get ('TMP', 'path'))
        self.temp_img__lbl = MyLabel  (self, rw =  9, cl = 1,         st = W, text = 'Изображение')
        self.temp_img__ent = MyEntry  (self, rw =  9, cl = 2,         st = W, text = conf.get ('TMP', 'image'))
        self.wind_sect_lbl = MyLabel  (self, rw = 10,                 st = W, text = 'Окно')
        self.wind_ttl__lbl = MyLabel  (self, rw = 11, cl = 1,         st = W, text = 'Заголовок')
        self.wind_ttl__ent = MyEntry  (self, rw = 11, cl = 2,         st = W, text = conf.get ('WINDOW', 'title'))
        self.wind_wdt__lbl = MyLabel  (self, rw = 12, cl = 1,         st = W, text = 'Ширина')
        self.wind_wdt__ent = MyEntry  (self, rw = 12, cl = 2,         st = W, text = conf.get ('WINDOW', 'width'))
        self.wind_hgt__lbl = MyLabel  (self, rw = 13, cl = 1,         st = W, text = 'Высота')
        self.wind_hgt__ent = MyEntry  (self, rw = 13, cl = 2,         st = W, text = conf.get ('WINDOW', 'height'))
        self.wind_xstp_lbl = MyLabel  (self, rw = 14, cl = 1,         st = W, text = 'Левый край')
        self.wind_xstp_ent = MyEntry  (self, rw = 14, cl = 2,         st = W, text = conf.get ('WINDOW', 'x_step'))
        self.wind_ystp_lbl = MyLabel  (self, rw = 15, cl = 1,         st = W, text = 'Верхний край')
        self.wind_ystp_ent = MyEntry  (self, rw = 15, cl = 2,         st = W, text = conf.get ('WINDOW', 'y_step'))
        self.tckt_sect_lbl = MyLabel  (self, rw = 16,                 st = W, text = 'Билеты')
        self.tckt_cnt__lbl = MyLabel  (self, rw = 17, cl = 1,         st = W, text = 'Количество')
        self.tckt_cnt__ent = MyEntry  (self, rw = 17, cl = 2,         st = W, text = conf.get ('TICKET', 'count'))
        self.tckt_strt_lbl = MyLabel  (self, rw = 18, cl = 1,         st = W, text = 'Начальный')
        self.tckt_strt_ent = MyEntry  (self, rw = 18, cl = 2,         st = W, text = conf.get ('TICKET', 'start'))
        self.qstn_sect_lbl = MyLabel  (self, rw = 19,                 st = W, text = 'Вопросы')
        self.qstn_cnt__lbl = MyLabel  (self, rw = 20, cl = 1,         st = W, text = 'Количество')
        self.qstn_cnt__ent = MyEntry  (self, rw = 20, cl = 2,         st = W, text = conf.get ('QUESTION', 'count'))
        self.qstn_strt_lbl = MyLabel  (self, rw = 21, cl = 1,         st = W, text = 'Начальный')
        self.qstn_strt_ent = MyEntry  (self, rw = 21, cl = 2,         st = W, text = conf.get ('QUESTION', 'start'))
        self.answ_sect_lbl = MyLabel  (self, rw = 22,                 st = W, text = 'Ответы')
        self.answ_cnt__lbl = MyLabel  (self, rw = 23, cl = 1,         st = W, text = 'Количество')
        self.answ_cnt__ent = MyEntry  (self, rw = 23, cl = 2,         st = W, text = conf.get ('ANSWER', 'count'))
        self.answ_strt_lbl = MyLabel  (self, rw = 24, cl = 1,         st = W, text = 'Начальный')
        self.answ_strt_ent = MyEntry  (self, rw = 24, cl = 2,         st = W, text = conf.get ('ANSWER', 'start'))
        self.lgc__sect_lbl = MyLabel  (self, rw = 25,                 st = W, text = 'Логика')
        self.lgc__err__lbl = MyLabel  (self, rw = 26, cl = 1,         st = W, text = 'Количество ошибок')
        self.lgc__err__ent = MyEntry  (self, rw = 26, cl = 2,         st = W, text = conf.get ('LOGIC', 'max_error'))
        
        self.delim_lbl     = MyLabel  (self, rw = 27,         cs = 3)
        self.save_bttn     = MyButton (self, rw = 28,                 st = E, text = '  Сохранить ', command = self.save)
        self.main_bttn     = MyButton (self, rw = 28, cl = 1,         st = N, text = 'Главное меню', command = self.main_menu)
        self.exit_bttn     = MyButton (self, rw = 28, cl = 2,         st = W, text = '    Выход   ', command = gui_exit)
        
    def save (self):
        '''Сохранение настроек'''
        conf.set ('FONT',     'name',      self.font_name_ent.get ())
        conf.set ('FONT',     'size',      self.font_size_ent.get ())
        conf.set ('DATABASE', 'path',      self.db___path_ent.get ())
        conf.set ('DATABASE', 'name',      self.db___name_ent.get ())
        conf.set ('TMP',      'path',      self.temp_path_ent.get ())
        conf.set ('TMP',      'image',     self.temp_img__ent.get ())
        conf.set ('WINDOW',   'title',     self.wind_ttl__ent.get ())
        conf.set ('WINDOW',   'width',     self.wind_wdt__ent.get ())
        conf.set ('WINDOW',   'height',    self.wind_hgt__ent.get ())
        conf.set ('WINDOW',   'x_step',    self.wind_xstp_ent.get ())
        conf.set ('WINDOW',   'y_step',    self.wind_ystp_ent.get ())
        conf.set ('TICKET',   'count',     self.tckt_cnt__ent.get ())
        conf.set ('TICKET',   'start',     self.tckt_strt_ent.get ())
        conf.set ('QUESTION', 'count',     self.qstn_cnt__ent.get ())
        conf.set ('QUESTION', 'start',     self.qstn_strt_ent.get ())
        conf.set ('ANSWER',   'count',     self.answ_cnt__ent.get ())
        conf.set ('ANSWER',   'start',     self.answ_strt_ent.get ())
        conf.set ('LOGIC',    'max_error', self.lgc__err__ent.get ())
        with open (CONF, 'w') as config:
            conf.write (config)
        gui_exit ()
        main ('conf')

    def main_menu (self):
        self.destroy ()
        self = MainMenu (self.master)
            
class Test (Frame):
    '''Тестирование'''
    def __init__ (self, master):
        super (Test, self).__init__ (master)
        self.questions = [0]
        for question in range (conf.getint ('QUESTION', 'count')):
            qn = question + conf.getint ('QUESTION', 'start')
            self.questions.append (Question (ticket = randrange (conf.getint ('TICKET', 'count')) + conf.getint ('TICKET', 'start'), number = qn))
        self.answers  = [0]
        self.errors   = [0]
        self.create_widgets ()
        self.get_question   ()
        self.grid           ()

    def create_widgets (self):
        '''Создание виджетов'''
        self.answer = StringVar ()
        self.answer.set (None)
        self.title_lbl = MyMessage (self, rw =  0, cs = 2)
        self.image_lbl = MyMessage (self, rw =  1, cs = 2,         image = None)
        self.quest_lbl = MyMessage (self, rw =  2, cs = 2,         width = 800)
        self.dlm_1_lbl = MyMessage (self, rw =  3, cs = 2)
        self.ans_1_rad = MyRadio   (self, rw =  4,         st = W, text = '1',    variable = self.answer, value = '1')
        self.ans_1_lbl = MyMessage (self, rw =  4, cl = 1, st = W, width = 800)
        self.ans_2_rad = MyRadio   (self, rw =  5,         st = W, text = '2',    variable = self.answer, value = '2')
        self.ans_2_lbl = MyMessage (self, rw =  5, cl = 1, st = W, width = 800)
        self.ans_3_rad = MyRadio   (self, rw =  6,         st = W, text = '3',    variable = self.answer, value = '3')
        self.ans_3_lbl = MyMessage (self, rw =  6, cl = 1, st = W, width = 800)
        self.ans_4_rad = MyRadio   (self, rw =  7,         st = W, text = '4',    variable = self.answer, value = '4')
        self.ans_4_lbl = MyMessage (self, rw =  7, cl = 1, st = W, width = 800)
        self.ans_5_rad = MyRadio   (self, rw =  8,         st = W, text = '5',    variable = self.answer, value = '5')
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
        self.good_answer = 0
        for answer in range (conf.getint ('ANSWER', 'count')):
            an = answer + conf.getint ('ANSWER', 'start')
            ao = Answer (ticket = question.ticket, question = question.number, number = an)
            if ao.is_true:
                self.good_answer = an
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
            self.image = Image.open (IMAGE)
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
        if self.answer.get () == 'None': return
        self.answers [0] += 1
        self.answers.append (int (self.answer.get ()))
        if int (self.answer.get ()) != self.good_answer:
            self.errors [0] += 1
            self.errors.append (self.questions [self.answers [0]])
        if self.answers [0] < conf.getint ('QUESTION', 'count'):
            self.get_question ()
        else:
            self.destroy ()
            self = Result (self.master, self.answers, self.errors)
        
    def main_menu (self):
        '''Выход в главное меню'''
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

    def result (self):
        '''Подводит итоги'''
        if self.errors [0] <= conf.getint ('LOGIC', 'max_error'):
            return 'Экзамен сдан'
        else:
            return 'Переэкзаменовка'

    def create_widgets (self):
        '''Создание виджетов'''
        self.title_lbl = MyMessage (self,                 cs = 2, text = 'Результаты')
        self.resul_lbl = MyMessage (self, rw = 1,         cs = 2, text = self.result ())
        self.delim_lbl = MyMessage (self, rw = 2,         cs = 2)
        self.more_bttn = MyButton  (self, rw = 3,         cs = 2, text = 'Просмотр ошибок',  command = self.more)
        self.main_bttn = MyButton  (self, rw = 4,                 text = 'Главное меню',     command = self.main_menu)
        self.exit_bttn = MyButton  (self, rw = 4, cl = 1,         text = '    Выход   ',     command = gui_exit)

    def more (self):
        '''Вывод подробностей'''
        self.destroy ()
        self = More (self.master, self.answers, self.errors)

    def main_menu (self):
        '''Выход в главное меню'''
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

    def create_widgets (self):
        '''Создание виджетов'''
        self.title_lbl = MyMessage (self,                 cs = 4,         text = 'Ошибки при проходжении теста')
        self.dlm_1_lbl = MyMessage (self, rw = 1,         cs = 4)
        self.cnt_1_lbl = MyMessage (self, rw = 2,         cs = 3, st = W, text = 'Количество ошибок:')
        self.cnt_2_lbl = MyMessage (self, rw = 2, cl = 3,                 text = self.errors [0])
        self.dlm_2_lbl = MyMessage (self, rw = 3,         cs = 4,         text = '')
        self.tck_0_lbl = MyMessage (self, rw = 4,                         text = 'Билет')
        self.qst_0_lbl = MyMessage (self, rw = 4, cl = 1,                 text = 'Вопрос')
        self.ans_0_lbl = MyMessage (self, rw = 4, cl = 2,                 text = 'Ваш ответ')
        self.ans_0_lbl = MyMessage (self, rw = 4, cl = 3,                 text = 'Верный ответ')
        rw = 5
        for question in self.errors[1:]:
            for answer in range (conf.getint ('ANSWER', 'count')):
                good_answer = answer + 1
                ao = Answer (ticket = question.ticket, question = question.number, number = good_answer)
                if ao.is_true: break
            MyMessage (self, rw = rw,         text = question.ticket)
            MyMessage (self, rw = rw, cl = 1, text = question.number)
            MyMessage (self, rw = rw, cl = 2, text = self.answers [question.number])
            MyMessage (self, rw = rw, cl = 3, text = good_answer)
            rw += 1
        self.main_bttn = MyButton (self, rw = rw,         cs = 3, text = 'Главное меню', command = self.main_menu)
        self.exit_bttn = MyButton (self, rw = rw, cl = 3,         text = '    Выход   ', command = gui_exit)

    def main_menu (self):
        '''Выход в главное меню'''
        self.destroy ()
        self = MainMenu (self.master)

main ()
