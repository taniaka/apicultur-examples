#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:
    from .. import secret
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from combination import Combination

class Word:

  PRONOUNS =  {
      'la':'directo',
      'las': 'directo',
      'le': 'indirecto',
      'les': 'indirecto',
      'lo': 'directo',
      'los': 'directo',
      'nos': 'directo o indirecto',
      'me': 'directo o indirecto',
      'se': 'directo o indirecto',
      'os': 'directo o indirecto',
      'te': 'directo o indirecto'
  }



  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  def __init__(self, word):
    self.word = word
    self.last_syllables = self.get_last(word)

    self.base_woord = word
    # self.first, self.second = None, None
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
    #TODO: cometodos                  
    return last_syllables

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

  def detect_enclitics(self):
    length = 0

    if self.last in self.PRONOUNS:
      self.enclitics.append(self.last)
      length += len(self.last)
      if self.second_last in self.PRONOUNS:
        self.enclitics.insert(0, self.second_last)
        length += len(self.second_last)    
        
      if ''.join(self.enclitics) == self.word:
        self.base_woord = self.second_last
        self.enclitics = [self.last]
      else:
        self.base_woord = self.word[0:-length]
      if self.enclitics[0] == 'nos':
        position1 = self.word.rfind('nos')
        position2 = self.word.rfind('monos')
        if position1 == position2 + 2:
          if position2 not in [0, 1]:
            self.base_woord = self.base_woord + 's'
     
    self.base_woord = self.del_accent(self.base_woord)
    return


  def detect_verbs(self):
    iig_infinitives = []
    lemmas = self.APICULTUR.lematiza2(word=self.base_woord)
    if lemmas:
      for lemma in lemmas['lemas']:
        category = lemma['categoria']
        if category[0] == 'V':
          self.infinitives.append(lemma['lema'])
          if category[0:3] in ['VMM', 'VMG', 'VMN']:
            self.is_valid_form = True
            iig_infinitives.append(lemma['lema'])
            
            if self.base_woord[-3:] == 'mos'and self.enclitics[0] == 'nos':
              position = self.word.rfind('nos')
              if self.word[position - 1] == 's':
                self.is_valid_form = False

    if self.base_woord != self.word and self.infinitives:
      if self.is_valid_form:
        self.infinitives = iig_infinitives        
    self.infinitives = list(set(self.infinitives))  

    # True, infinitives => this is a valid verbal form that can take enclitics
    # False, infinitives => this is a verbal form but it can't take enclitics
    # False, no infinitives => this is not a verb
    return

  def analyze_word(self):
    #TODO: idos, comeros, comenos                 
    print(u'Tu palabra es: {}.'.format(self.word.upper()))    
    if len(self.last_syllables) == 1:
      print(u'\tTu palabra solo tiene una sílaba '
            u'y no puede tener enclíticos, intenta con otra palabra.')
      return
    self.second_last, self.last = self.last_syllables
    self.detect_enclitics()
    self.detect_verbs()
    if len(self.enclitics) == 2 and self.infinitives:
      self.combination = Combination(''.join(self.enclitics))

    self.print_results()
    return

  def print_results(self):
    if not self.infinitives:
      #TODO: if base_woord shorter than word, check word for verb (e.g.'trabajamos')

      print(u'\tParece que "{}" no es un verbo.'.
            format(self.word))

    else:
      if self.enclitics == ['se'] and self.is_valid_form:
        print(u'\tTienes un verbo con un pronombre enclítico "se" reflexivo: {}.'
              .format(self.word))
        return   
      else:      
        if len(self.infinitives) == 1:
          print(u'\tTienes un verbo: {}.'.format(self.infinitives[0]))
        else:
          print(u'\tTienes un verbo que podría ser uno de los siguientes: {}.'
                .format(', '.join(self.infinitives)))

        
      if not self.enclitics:
        print(u'\tNo se han detectado enclíticos.')

      else:
        if len(self.enclitics) == 1:
          print(u'\tTienes un enclítico de tipo complemento {}: {}.'.
                format(self.PRONOUNS[self.last], self.last))

        elif len(self.enclitics) == 2:
          print(u"\tTienes dos enclíticos:")
          if self.second_last == "se":
            print(u"\t\tEl primero es un complemento {}: {}, "
                  u"sustituyendo al pronombre 'le' o 'les'.".
                  format(self.PRONOUNS[self.second_last], self.second_last))
          else:
            print(u"\t\tEl primero es un complemento {}: {}.".
                  format(self.PRONOUNS[self.second_last], self.second_last))      
          print(u"\t\tEl segundo es un complemento {}: {}.".
                format(self.PRONOUNS[self.last], self.last))
          print(self.combination.message)

        if not self.is_valid_form:
          print(u'\tSin embargo, te advertimos que los enclíticos '
                u'deberían usarse solo con infinitivos, gerundios '
                u'e imperativos. En algunas regiones, por ejemplo '
                u'en Asturias, los pronombres pueden posponer al indicativo '
                u'y subjuntivo, pero en el castellano estándar está en desuso.')


def validate_word(word):
  word = word.strip()
  if not word.isalpha() or not word.find(' ') or word == '':
    print(u'Parece que no es una palabra.'
          'Vuelve a intentar.')
    return
  else:
    Word(word).analyze_word()
  return

validate_word(u'vámosnos')
validate_word(u'robárlole')
validate_word(u'vámonos')
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

