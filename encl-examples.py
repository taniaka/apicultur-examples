#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from encliticos.word import Word

def validate_word(word):
  word = word.strip()
  if not word.isalpha() or not word.find(' ') or word == '':
    print(u'Parece que no es una palabra.'
          u'Vuelve a intentar.')
    return
  else:
    Word(word).analyze_word()
  return

validate_word(u'pregúntatela')
validate_word(u'tomándoselas')
validate_word(u'acércamelos')
validate_word(u'robárlole')
validate_word(u'mangárleles')
validate_word(u'sacármete')
validate_word(u'diciéndomese')
validate_word(u'tomartete')
validate_word(u'vámonos')
validate_word(u'vámosnos')
validate_word(u'démosela')
validate_word(u'dámossela')
validate_word(u'acercaos')
validate_word(u'acercados')
validate_word(u'comedos')
validate_word(u'comeos')
validate_word(u'salíos')
validate_word(u'reíos')
validate_word(u'acercarselo')
validate_word(u'acercársele')
validate_word(u'acercasela')
validate_word(u'acérquensela')
validate_word(u'acérquensele')
validate_word(u"estate")
validate_word(u"estáte")
validate_word(u'dime')
validate_word(u'idos')
validate_word(u'seguirle')
validate_word(u'rompiéndonos')
validate_word(u'rompiendonos')
validate_word(u'fíjate')
validate_word(u'fijate')
validate_word(u'irse')
validate_word(u'sumándose')
validate_word(u'tirándonos')
validate_word(u'preguntaros')
validate_word(u'comeros')
validate_word(u'vélale')
validate_word(u'cómola')
validate_word(u'preguntámostelo')
validate_word(u'comemos')
validate_word(u'desayuna')
validate_word(u'bailamos')
validate_word(u'dfghdfhfghmela')
validate_word(u'majos')
validate_word(u'mala')
validate_word(u'verde')
validate_word(u'las')
validate_word(u'123')
validate_word(u'dame1la')
validate_word(u' ')
validate_word(u'')

print(u'\nEscribe tu palabra aquí.'
      u'Si no quieres seguir, escribe QUIT.')

while True:
  try:
    input = raw_input
  except NameError:
    pass
  word = input(u'>>> ')
  try:
    word = unicode(word, 'utf-8')
  except:
    word = u"{}".format(word)
    
  if word.upper() == u'QUIT':
    sys.exit()
  else:
    validate_word(word)
