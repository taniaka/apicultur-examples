#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)


# un pronombre no puede combinarse consigo mismo
# 'le' y 'les' no pueden ocupar ninguna de las dos posiciones
# 'se' no puede ocupar la segunda posición
# 'la', 'lo', 'los', 'las' no pueden ocupar la primera posición
# 'me' y 'nos' no pueden preceder a 'te' y 'os'
# 'se' no puede preceder a 'te', 'me', 'nos', 'os'  (o sí???)
# 'me' y 'nos' no se pueden combinar entre ellos (o sí???)
# 'te' y 'os' no se pueden combinar entre ellos (o sí???)

class Word:

  PRONOUNS =   {'la':'directo',
                'las': 'directo',
                'le': 'indirecto',
                'les': 'indirecto',
                'lo': 'directo',
                'los': 'directo',
                'nos': 'de tipo indefinido (directo o indirecto)',
                'me': 'de tipo indefinido (directo o indirecto)',
                'se': 'indirecto',
                'os': 'de tipo indefinido (directo o indirecto)',
                'te': 'de tipo indefinido (directo o indirecto)'
              }

  # VALID_COMBINATIONS = ['melo', 'mela', 'melos', 'melas',
  #                       'telo', 'tela', 'telos', 'telas',
  #                       'teme', 'tenos',
  #                       'selo', 'sela', 'selos', 'selas',
  #                       'noslo', 'nosla', 'noslos', 'noslas',
  #                       'oslo' 'osla', 'oslos', 'oslas',
  #                       'osme', 'osnos'
  #                       ]


  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  def __init__(self, word):
    self.word = word
    self.root_word = word
    self.last_syllables = self.get_last(word)
    if len(self.last_syllables) < 2:
      self.last_syllables.insert(0, None) 
    self.second_last, self.last = self.last_syllables

    self.enclitics = []
    self.infinitives = []
    self.is_valid_form = False

  def get_last(self, word):
    last_syllables = []
    syllabized = self.APICULTUR.silabeame(word=word)
    syllables = syllabized['palabraSilabeada'].split('=')
    for num in range(2):
      index = -(num+1)
      try:
        last_syllables.insert(0,syllables[index])
      except:
        break
    last_syllables = ['os' if syllable == 'ros' 
                      else syllable for syllable in last_syllables]
    
    return last_syllables


  def detect_enclitics(self):
    length = 0

    if self.last in self.PRONOUNS:
      self.enclitics.append(self.last)
      length += len(self.last)
      if self.second_last in self.PRONOUNS:
        self.enclitics.insert(0, self.second_last)
        length += len(self.second_last)    
        
      if ''.join(self.enclitics) == self.word:
        self.root_word = self.second_last
        self.enclitics = [self.last]
      else:
        self.root_word = self.word[0:-length]
        
    self.root_word = self.del_accent(self.root_word)
    return


  def del_accent(self, my_word):
    new_word = my_word
    accents = {u'á': 'a', u'ú':'u', u'í':'i', u'é':'e', u'ó':'o'}
    last_two = self.get_last(my_word)
    if my_word[-1] == 'r':
      syllable = last_two[-1]
    else:
      syllable = last_two[0]
    for key, value in accents.items():
      if key in syllable:
        new_syllable = syllable.replace(key, value)
        new_word = my_word.replace(syllable, new_syllable)    
        break
    return new_word   


  def detect_verbs(self):
    iig_infinitives = []

    lemmas = self.APICULTUR.lematiza2(word=self.root_word)
    if lemmas:
      for lemma in lemmas['lemas']:
        category = lemma['categoria']
        if category[0] == 'V':
          self.infinitives.append(lemma['lema'])
          if category[0:3] in ['VMM', 'VMG', 'VMN']:
            iig_infinitives.append(lemma['lema'])
            self.is_valid_form = True

    if self.infinitives and self.is_valid_form and self.root_word != self.word:
      self.infinitives = iig_infinitives

    self.infinitives = list(set(self.infinitives))  

    # True, infinitives => this is a valid verbal form that can take enclitics
    # False, infinitives => this is a verbal form but it can't take enclitics
    # False, no infinitives => this is not a verb
    return


  def analyze_word(self):

    print(u'Tu palabra es: {}.'.format(self.word.upper()))
    
    if None in self.last_syllables:
      print(u'\tTu palabra solo tiene una sílaba '
            u'y no puede tener enclíticos, intenta con otra palabra.')
      return
    
    self.detect_enclitics()
    self.detect_verbs()

    if not self.infinitives:
      #TODO: if root_word shorter than word, check word for verb (e.g.'trabajamos')
      #or find another way to deal with 1 persona Plural
      #TODO: palabras de tipo 'vámonos', 'idos', 'podemos', 'podamos'
      print(u'\tParece que "{}" no es un verbo.'.
            format(self.word))

    else:

      if not self.is_valid_form or not self.enclitics:
        if len(self.infinitives) == 1:
          print(u'\tTienes un verbo: {}.'.format(self.infinitives[0]))
        else:
          print(u'\tTienes un verbo que podría ser uno de los siguientes: {}.'
                .format(', '.join(self.infinitives)))
        print(u'\tNo se han detectado enclíticos.')

      else:

        if self.enclitics == ['se'] and self.is_valid_form:
          print('Tienes un verbo reflexivo: {}.'
                .format(self.word))
        
        else:
          print(u'\tTienes un verbo: {}.'.format(self.infinitives[0]))

          if len(self.enclitics) == 1:
            print(u'\tTienes un enclítico de tipo complemento {}: {}.'.
                  format(self.PRONOUNS[self.last], self.last))

          elif len(self.enclitics) == 2:
            print(u"\tTienes dos enclíticos:")
            if self.second_last == "se":
              print(u"\t\tEl primero es un complemento indirecto: {}, "
                    u"sustituyendo al pronombre 'le' o 'les'.".
                    format(self.second_last))
            else:
              print(u"\t\tEl primero es un complemento indirecto: {}.".
                    format(self.second_last))      
            print(u"\t\tEl segundo es un complemento directo: {}.".
                  format(self.last))



def validate_word(word):
  word = word.strip()
  if not word.isalpha() or not word.find(' ') or word=='':
    print(u'Parece que no es una palabra.'
          'Vuelve a intentar.')
    return
  else:
    Word(word).analyze_word()
  return

validate_word(u'dime')
validate_word(u'preguntaros')
validate_word(u'dárosla')
validate_word(u'tomárselas')
validate_word(u'pónselas')
validate_word(u'pregúntatela')
validate_word(u'sálvanos')
validate_word(u'acercaros')
validate_word(u'acercaos')
validate_word(u'seguirle')
validate_word(u'seguirlo')
validate_word(u'irse')
validate_word(u'celebrarse')
validate_word(u'trabajo')
validate_word(u'burros')
validate_word(u'majos')
validate_word(u'mala')
validate_word(u'luz')
validate_word(u'las')
validate_word(u'verde')
validate_word(u'123')
validate_word(u' ')
validate_word(u'')


print(u'Escribe tu palabra aquí.'
      u'Si no quieres seguir, escribe QUIT.')

while True:
  word = input(u'>>> ')
  word = u"{}".format(word)
  if word.upper() == 'QUIT':
    sys.exit()
  else:
    validate_word(word)

