#!/bin/python3

from   sys     import platform as OS
import sqlite3 as lite

if OS == 'linux': CON = lite.connect ('/data/git/PDD/PDD/expluatation.db')
else:             CON = lite.connect ('W:/Общая/VAA/PDD/expluatation.db')
CUR = CON.cursor ()

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
    try:    self.image   = CUR.execute ('SELECT image   FROM questions WHERE id = %d' % self.id).fetchone () [0]
    except: self.image   = None
    try:    self.text    = CUR.execute ('SELECT text    FROM questions WHERE id = %d' % self.id).fetchone () [0]
    except: self.text    = None
    try:    self.comment = CUR.execute ('SELECT comment FROM questions WHERE id = %d' % self.id).fetchone () [0]
    except: self.comment = None

  def __str__ (self):
    if self.image: is_image = True
    else:          is_image = False
    return '''
id:        %d
ticket:    %d
number:    %d
is_image:  %s
text:      %s
comment:   %s
is_db:     %s
''' % (self.id, self.ticket, self.number, is_image, self.text, self.comment, str (self.is_db ()))

  def is_db (self):
      if CUR.execute ('SELECT * FROM questions WHERE id = %d' % self.id).fetchone ():
        return True
      else:
        return False

  def write (self):
    if self.is_db ():
      print ('Question now in db.')
      return
    CUR.execute ('INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?)', (self.id, self.ticket, self.number, self.text, self.image, self.comment))
    CON.commit ()
    self.__init__ (ident = self.id)

  def update (self, field, value):
    if not self.is_db ():
      print ('Question not in db.')
      return
    CUR.execute ('UPDATE questions SET %s = "%s" WHERE id = %d' % (field, value, self.id))
    CON.commit ()
    self.__init__ (ident = self.id)

  def delete (self):
    if not self.is_db ():
      print ('Question not in db.')
      return
    CUR.execute ('DELETE FROM questions WHERE id = %d' % self.id)
    CON.commit ()
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

  def delete (self):
    if not self.is_db ():
      print ('Answer now in db.')
      return
    CUR.execute ('DELETE FROM answers WHERE id = %d' % self.id)
    CON.commit ()
    self.__init__ (ticket = self.ticket, question = self.question, number = self.number)

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
      
'''
for ticket in range (40):
  tn = ticket + 1
  print (tn)
  if tn < 10: tnn = '0%d' % tn
  else:       tnn = str (tn)
  for question in range (20):
    qn = question + 1
    print (tn, qn)
    if qn < 10: qnn = '0%d' % qn
    else:       qnn = str (qn)
    qo = Question (ticket = tn, number = qn)
    #new_text    = input ('text:    ' + str (qo.text)    + ': ')
    new_text    = None
    #new_comment = input ('comment: ' + str (qo.comment) + ': ')
    new_comment = None
    try:
      if OS == 'linux': image = readImage ('/data/git/PDD/PDD/forklift_images/%d-%d.jpg' % (tn, qn))
      else:             image = readImage ( 'W:/Общая/VAA/PDD/forklift_images/%d-%d.jpg' % (tn, qn))
      binary = lite.Binary (image)
    except:
      binary = None
    if new_text:
      if new_text != ' ':
        qo.write ()
        qo.update ('text', new_text)
        if new_comment: qo.update ('comment', new_comment)
        CUR.execute ('UPDATE questions SET image = (?) WHERE id = %d' % qo.id, (binary,) )
    #  else:
    #    qo.delete ()
    CUR.execute ('UPDATE questions SET image = (?) WHERE id = %d' % qo.id, (binary,) )
    CON.commit ()
    qo = Question (ident = qo.id)
    print (qo)
    for answer in range (5):
      an = answer + 1
      print (tn, qn, an)
      ao = Answer (ticket = tn, question = qn, number = an)
      #new_text = input (str (ao.text) + ': ')
      new_text = None
      if new_text:
        if new_text != ' ':
          ao.write ()
          ao.update ('text', new_text)
        else:
          ao.delete ()
      print ()
    #try:    good = int (input ('Укажите номер ответа: '))
    #except: good = None
    good = None
    for answer in range (5):
      an = answer + 1
      print (tn,qn,an)
      ao = Answer (ticket = tn, question = qn, number = an)
      if good:
        if an == good: ao.update ('is_true', 1)
        else:          ao.update ('is_true', 0)
      ao = Answer (ident = ao.id)
      print (ao)

if OS == 'linux': image = readImage ('/data/git/PDD/PDD/images/text.gif')
else:             image = readImage ( 'W:/Общая/VAA/PDD/images/text.gif')
binary = lite.Binary (image)
CUR.execute ('UPDATE questions SET image   = (?)  WHERE image   is null;', (binary,) )
CUR.execute ('UPDATE questions SET comment = null WHERE comment =  " ";')
CON.commit ()
'''

tn = 0
qn = 0
an = 0

if OS =='linux': task = open ('/data/git/PDD/PDD/b-2011.txt', 'r')
else:            task = open ('W:/Общая/VAA/PDD/b-2011.txt',  'r', encoding = 'utf-8')
lines = task.readlines ()
task.close ()

for line in lines:
  if   line [0] == 'T': tn = int (line [1:3])
  elif line [0] == 'Q':
    qn = int (line [1:2])
    qo = Question (ticket = tn, number = qn)
    qo.write ()
    qo.update ('text', line [3:].replace ('\n', ''))
    if OS == 'linux':
      try:    image = readImage ('/data/git/PDD/PDD/expluatation_images/%d_%d.jpg' % (tn, qn))
      except: image = readImage ('/data/git/PDD/PDD/images/text.gif')
    else:
      try:    image = readImage ('W:/Общая/VAA/PDD/expluatation_images/%d_%d.jpg' % (tn, qn))
      except: image = readImage ('W:/Общая/VAA/PDD/images/text.gif')
    binary = lite.Binary (image)
    CUR.execute ('UPDATE questions SET image = (?) WHERE id = %d' % qo.id, (binary,) )
    CON.commit ()
    print (qo)
  elif line [0] == 'C':
    comment = line [2:]
    qo.update ('comment', comment)
    print (qo)
  elif line [0] == 'A':
    an = int (line [1:2])
    ao = Answer (ticket = tn, question = qn, number = an)
    ao.write ()
    ao.update ('text', line [3:].replace ('\n', ''))
    print (ao)
  elif line [0] == 'R':
    an = line [1]
    ao = Answer (ticket = tn, question = qn, number = an)
    ao.update ('is_true', 1)
    print (ao)

CON.close ()
