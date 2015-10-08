#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from encliticos.word import Word

if __name__ == '__main__':

  def get_word_info(my_word):
    print(u'\nTu palabra es: {}.'.format(my_word.upper()))
    word = Word(my_word)
    word.analyze_word()

    if not word.structures:
      print(u'\tParece que "{}" no es un verbo.'.
            format(my_word))
    else:
      for num, structure in enumerate(word.structures):       
        if len(word.structures) > 1:        
          print(u'Opción {}.'.format(num+1))
        print(structure.message)

  # get_word_info(u'acércamelos')
  # get_word_info(u'acentuamelose')
  # get_word_info(u'tomársemela')
  # get_word_info(u'tomándosemele')
  # get_word_info(u'ponganselasme')
  # get_word_info(u'acentúaseseme')
  # get_word_info(u'pregúntatela')
  # get_word_info(u'tomándoselas')
  # get_word_info(u'robárlole')
  # get_word_info(u'mangárleles')
  # get_word_info(u'sacármete')
  # get_word_info(u'diciéndomese')
  # get_word_info(u'tomartete')
  # get_word_info(u'vámonos')
  # get_word_info(u'vámosnos')
  # get_word_info(u'démosela')
  # get_word_info(u'dámossela')
  # get_word_info(u'acercaos')
  # get_word_info(u'acercados')
  # get_word_info(u'comedos')
  # get_word_info(u'comeos')
  # get_word_info(u'salíos')
  # get_word_info(u'reíos')
  # get_word_info(u'acercarselo')
  # get_word_info(u'acercársele')
  # get_word_info(u'acercasela')
  # get_word_info(u'acérquensela')
  # get_word_info(u'acérquensele')
  # get_word_info(u"estate")
  # get_word_info(u"estáte")
  # get_word_info(u'dime')
  # get_word_info(u'idos')
  # get_word_info(u'seguirle')
  # get_word_info(u'rompiéndonos')
  # get_word_info(u'rompiendonos')
  # get_word_info(u'fíjate')
  # get_word_info(u'fijate')
  # get_word_info(u'irse')
  # get_word_info(u'sumándose')
  # get_word_info(u'tirándonos')
  # get_word_info(u'preguntaros')
  # get_word_info(u'comeros')
  # get_word_info(u'vélale')
  # get_word_info(u'cómola')
  # get_word_info(u'preguntámostelo')
  # get_word_info(u'comemos')
  # get_word_info(u'desayuna')
  # get_word_info(u'bailamos')
  # get_word_info(u'dfghdfhfghmela')
  # get_word_info(u'majos')
  # get_word_info(u'mala')
  # get_word_info(u'verde')

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
      get_word_info(word)
