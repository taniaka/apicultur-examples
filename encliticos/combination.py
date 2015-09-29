#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Combination:


  ENCLITICS = ('se', 'te', 'os', 'me', 'nos',
              'le', 'les', 'lo', 'la', 'los', 'las')

  # no funciona:
  # Matrix = [['A' for encl in ENCLITICS] for encl in ENCLITICS]

  Matrix = [['A' for i in range(11)] for i in range(11)]

  for x in range(5):
    Matrix[x][x] = 'R'

  for y in range(1,11):
    Matrix[0][y] = None

  for x in range(1,5):
    for y in range(7,11):
      Matrix[x][y] = None

  for x in range(1,5):
    for y in range(5,7):
      Matrix[x][y] = 'I'
  
  for x in range(1,3):
    for y in range(3,5):
      Matrix[x][y] = 'I'    

  for x in range(5,11):
    for y in range(5,11):
      Matrix[x][y] = 'X'

  Matrix[1][2] = 'P'
  Matrix[2][1] = 'P'
  Matrix[3][4] = 'P'
  Matrix[4][3] = 'P'

  ERRORS = {
    None: u'\n\tTu combinación es válida (explicar por qué).',
    'I':  u'\n\tTu combinación puede ser un leísmo o puede '
          u'tener un dativo ético (explicar). ',
    'A':  u'\n\tTu combinación es inválida, alteración de orden. ',
    'R':  u'\n\tNo se puede repetir el mismo enclítico. ',
    'P':  u'\n\tNo se pueden combinar dos primeras o dos '
          u'segundas personas. ',
    'X':  u'\n\tCombinación inválida de dos terceras personas. ',
    'T':  u'\n\tEstá combinación no es válida. '
          u'Mensaje explicando cómo combinar 3 enclíticos. '

  }


  # VALID_MESSAGE = [ u"\n\tAquí tendremos un mensaje explicando "\
  #                   u"por qué esta combinación es válida y cómo "\
  #                   u"hay que combinar dos enclíticos.",
  #                   u"\n\tMensaje explicando por qué esta combinación "\
  #                   u"es correcta y cómo combinar 3 enclíticos"
  # ]                  

  # INVALID_MESSAGE =[u"\n\tSin embargo, esta combinación no es válida.\n\t",
  #                   u"\n\tEsta combinación no es válida. "\
  #                   u"\n\tMensaje sobre cómo combinar 3 enclíticos.\n\t"
  # ]                  
                        

  def __init__(self, combination):    
    self.combination = combination
    self.error, self.message = self.get_error()

  def get_error(self):
    last_two = self.combination[-2:]
    prelast = self.ENCLITICS.index(last_two[0])
    last = self.ENCLITICS.index(last_two[1])
    error = self.Matrix[prelast][last]
    message = self.ERRORS[error]

    if len(self.combination) == 3:
      first = self.combination[0]
      if first not in ['se', 'me', 'te', 'nos', 'os'] or first in last_two:
        if not error:
          error = 'T'
          message = ''
        else:
          message += 'Además tienes otro problema.'  
        message += self.ERRORS['T']
    return error, message

























