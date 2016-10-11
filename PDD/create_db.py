#!/bin/python3

import sqlite3 as lite

CON  = lite.connect ('W:/Общая/VAA/python/my_progs/PDD/PDD.db')
CUR  = CON.cursor ()

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

  def update (self, field, value):
    if not self.is_db ():
      print ('Question not in db.')
      return
    CUR.execute ('UPDATE questions SET %s = "%s" WHERE id = %d' % (field, value, self.id))
    CON.commit ()
    self.__init__ (ident = self.id)

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
    try:    self.text    = CUR.execute ('SELECT text    FROM answers WHERE id = %d' % self.id).fetchone () [0]
    except: self.text    = None
    try:    self.is_true = CUR.execute ('SELECT is_true FROM answers WHERE id = %d' % self.id).fetchone () [0]
    except: self.is_true = 0

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

  def update (self, field, value):
    if not self.is_db ():
      print ('Answer not in db.')
      return
    CUR.execute ('UPDATE answers SET %s = "%s" WHERE id = %d' % (field, value, self.id))
    CON.commit ()
    self.__init__ (ident = self.id)

def readImage (filename):
  try:
    fin = open (filename, 'rb')
    img = fin.read ()
    return img
  except IOError as e:
    img = None
  finally:
    if fin:
      fin.close ()
      
for ticket in range (1):
  tn = ticket + 31
  print (tn)
  if tn < 10: tnn = '0%d' % tn
  else:       tnn = str (tn)
  for question in range (20):
    qn = question + 1
    print (tn, qn)
    if qn < 10: qnn = '0%d' % qn
    else:       qnn = str (qn)
    qo = Question (ticket = tn, number = qn)
    new_text = input (qo.text + ': ')
    #new_text = None
    try:
      image  = readImage ('W:/Общая/VAA/PDD/images/Pdd_%s_%s.jpg' % (tnn, qnn))
      binary = lite.Binary (image)
    except:
      binary = None
    CUR.execute ('UPDATE questions SET image = (?) WHERE id = %d' % qo.id, (binary,) )
    CON.commit ()
    if new_text: qo.update ('text', new_text)
    qo = Question (ident = qo.id)
    print (qo)
    for answer in range (5):
      an = answer + 1
      print (tn, qn, an)
      ao = Answer (ticket = tn, question = qn, number = an)
      new_text = input (str (ao.text) + ': ')
      #new_text = None
      if new_text:
        ao.write ()
        ao.update ('text', new_text)
      print ()
    try:    good = int (input ('Укажите номер ответа: '))
    except: good = None
    #good = None
    for answer in range (5):
      an = answer + 1
      print (tn,qn,an)
      ao = Answer (ticket = tn, question = qn, number = an)
      if good:
        if an == good: ao.update ('is_true', 1)
        else:          ao.update ('is_true', 0)
      ao = Answer (ident = ao.id)
      print (ao)

image  = readImage ('W:/Общая/VAA/PDD/images/text.gif')
binary = lite.Binary (image)
CUR.execute ('UPDATE questions SET image = (?)  WHERE image is null;', (binary,) )
CUR.execute ('UPDATE answers   SET text  = null WHERE text  =  " ";')
CON.commit ()

CON.close ()
