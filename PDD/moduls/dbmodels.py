#!/bin/python3

from config    import settings as CONF
from functions import write_log
from sqlite3   import connect

class Question ():
  '''Вопросы'''
  def __init__ (self, ident = 0, ticket = 0, number = 0):
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
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
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      ident = CUR.execute ('SELECT * FROM questions WHERE id = %d' % self.id).fetchone ()
    if ident:
      return True
    else:
      return False

  def write (self):
    if self.is_db ():
      print ('Question now in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('INSERT INTO questions VALUES (?, ?, ?, ?, ?)', (self.id, self.ticket, self.number, self.text, self.image))
      CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Write question with id %d' % self.id)

  def update (self, field, value):
    if not self.is_db ():
      print ('Question not in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('UPDATE questions SET %s = "%s" WHERE id = %d' % (field, value, self.id))
      CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Update question with id %d' % self.id)

  def delete (self):
    if not self.is_db ():
      print ('Question not in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('DELETE FROM questions WHERE id = %d' % self.id)
      CON.commit ()
    write_log ('Delete question with id %d' % self.id)
    self.__init__ (ticket = self.ticket, number = self.number)

class Answer ():
  '''Варианты ответов'''
  def __init__ (self, ident = 0, ticket = 0, question = 0, number = 0):
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
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
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      ident = CUR.execute ('SELECT * FROM answers WHERE id = %d' % self.id).fetchone ()
    if ident:
      return True
    else:
      return False

  def write (self):
    if self.is_db ():
      print ('Answer now in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('INSERT INTO answers VALUES (?, ?, ?, ?, ?, ?)', (self.id, self.ticket, self.question, self.number, self.is_true, self.text))
      CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Write answer with id %d' % self.id)

  def update (self, field, value):
    if not self.is_db ():
      print ('Answer not in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('UPDATE answers SET %s = "%s" WHERE id = %d' % (field, value, self.id))
      CON.commit ()
    self.__init__ (ident = self.id)
    write_log ('Update answer with id %d' % self.id)

  def delete (self):
    if not self.is_db ():
      print ('Answer now in db.')
      return
    with connect (CONF.get ('FILES', 'db')) as CON:
      CUR = CON.cursor ()
      CUR.execute ('DELETE FROM answers WHERE id = %d' % self.id)
      CON.commit ()
    write_log ('Delete answer with id %d' % self.id)
    self.__init__ (ticket = self.ticket, question = self.question, number = self.number)
