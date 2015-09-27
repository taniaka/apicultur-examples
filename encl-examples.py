#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from encliticos.word import Word

if __name__ == '__main__':

  Word(u'acércamelos').analyze_word()
  Word(u'acentuamelose').analyze_word()
  Word(u'tomársemela').analyze_word()
  Word(u'tomándosemele').analyze_word()
  Word(u'ponganselasme').analyze_word()
  Word(u'acentúaseseme').analyze_word()
  Word(u'pregúntatela').analyze_word()
  Word(u'tomándoselas').analyze_word()
  Word(u'robárlole').analyze_word()
  Word(u'mangárleles').analyze_word()
  Word(u'sacármete').analyze_word()
  Word(u'diciéndomese').analyze_word()
  Word(u'tomartete').analyze_word()
  Word(u'vámonos').analyze_word()
  Word(u'vámosnos').analyze_word()
  Word(u'démosela').analyze_word()
  Word(u'dámossela').analyze_word()
  Word(u'acercaos').analyze_word()
  Word(u'acercados').analyze_word()
  Word(u'comedos').analyze_word()
  Word(u'comeos').analyze_word()
  Word(u'salíos').analyze_word()
  Word(u'reíos').analyze_word()
  Word(u'acercarselo').analyze_word()
  Word(u'acercársele').analyze_word()
  Word(u'acercasela').analyze_word()
  Word(u'acérquensela').analyze_word()
  Word(u'acérquensele').analyze_word()
  Word(u"estate").analyze_word()
  Word(u"estáte").analyze_word()
  Word(u'dime').analyze_word()
  Word(u'idos').analyze_word()
  Word(u'seguirle').analyze_word()
  Word(u'rompiéndonos').analyze_word()
  Word(u'rompiendonos').analyze_word()
  Word(u'fíjate').analyze_word()
  Word(u'fijate').analyze_word()
  Word(u'irse').analyze_word()
  Word(u'sumándose').analyze_word()
  Word(u'tirándonos').analyze_word()
  Word(u'preguntaros').analyze_word()
  Word(u'comeros').analyze_word()
  Word(u'vélale').analyze_word()
  Word(u'cómola').analyze_word()
  Word(u'preguntámostelo').analyze_word()
  Word(u'comemos').analyze_word()
  Word(u'desayuna').analyze_word()
  Word(u'bailamos').analyze_word()
  Word(u'dfghdfhfghmela').analyze_word()
  Word(u'majos').analyze_word()
  Word(u'mala').analyze_word()
  Word(u'verde').analyze_word()
  Word(u'las').analyze_word()

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
      Word(word).analyze_word()
