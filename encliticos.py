#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)


pronouns =   {'la':'directo',
              'las': 'directo',
              'le': 'indirecto',
              'les': 'indirecto',
              'lo': 'directo',
              'los': 'directo',
              'nos': 'de tipo indefinido (directo o indirecto)',
              'me': 'de tipo indefinido (directo o indirecto)',
              'se': 'de tipo indefinido (directo o indirecto)',
              'os': 'de tipo indefinido (directo o indirecto)',
              'te': 'de tipo indefinido (directo o indirecto)'
            }


apicultur = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")


def lematize(word):
  infinitives = []
  lemmas = apicultur.lematiza2(word=word)
  if lemmas:
    for lemma in lemmas['lemas']:
      category = lemma['categoria']
      if category[0] == 'V':
        infinitives.append(lemma['lema'])
    infinitives = list(set(infinitives))
  return infinitives    


def get_last(word, number):
  last_syllables = []
  syllabized = apicultur.silabeame(word=word)
  syllables = syllabized['palabraSilabeada'].split('=')
  for num in range(number):
    index = -(num+1)
    try:
      last_syllables.insert(0,syllables[index])
    except:
      break
  return last_syllables


def del_accent(word):
  new_word = word
  accents = {u'á': 'a', u'ú':'u', u'í':'i', u'é':'e', u'ó':'o'}
  last_two = get_last(word, 2)
  if word[-1] == 'r':
    syllable = last_two[-1]
  else:
    syllable = last_two[0]
  for key, value in accents.items():
    if key in syllable:
      new_syllable = syllable.replace(key, value)
      new_word = word.replace(syllable, new_syllable)    
      break
  return new_word   


def detect_enclitics(word, last, second_last):
  enclitics = []
  length = 0
  verb = word

  if last in pronouns:
    if last != 'se':
      enclitics.append(last)
      length += len(last)
      if second_last in pronouns:
        enclitics.insert(0, second_last)
        length += len(second_last)
    if ''.join(enclitics) == word:
      verb = None
    else:       
      verb = word[0:-length]
      verb = del_accent(verb)

  return verb, enclitics  


def analyze_word(word):
  if word == '' or word == ' ':
    print('No has introducido nada, vuelve a intentar.')
    return

  print(u'Tu palabra es: {}.'.format(word.upper()))
  
  last_syllables = get_last(word, 2)
  last_syllables = ['os' if syllable == 'ros' else syllable for syllable in last_syllables]
  if len(last_syllables) < 2:
    print(u'\tTu palabra solo tiene una sílaba '
          u'y no puede tener enclíticos, intenta con otra palabra.')
    return


  last = last_syllables[-1]
  second_last = last_syllables[-2]
  verb, enclitics = detect_enclitics(word, last, second_last)

  lemas = lematize(verb)


  if not lemas:
    print(u'\tParece que "{}" no es un verbo.'.
          format(word))

  else:

    if len(lemas) == 1:
      print(u'\tTienes un verbo: {}.'.format(lemas[0]))
    else:
      print(u'\tTienes un verbo que podría ser uno de los siguientes: {}.'.format(', '.join(lemas)))  

    if not enclitics:
      print(u'\tNo se han detectado enclíticos.')

    elif len(enclitics) == 1:
      print(u'\tTienes un enclítico de tipo complemento {}: {}.'.
            format(pronouns[last], last))

    elif len(enclitics) == 2:
      print(u"\tTienes dos enclíticos:")
      if second_last == "se":
        print(u"\t\tEl primero es un complemento indirecto: {}, "
              u"sustituyendo al pronombre 'le' o 'les'.".
              format(second_last))
      else:
        print(u"\t\tEl primero es un complemento indirecto: {}.".
              format(second_last))      
      print(u"\t\tEl segundo es un complemento directo: {}.".
            format(last))

analyze_word(u"dime")
analyze_word(u"preguntaros")
analyze_word(u"dárosla")
analyze_word(u"tomárselas")
analyze_word(u"pónselas")
analyze_word(u"pregúntatela")
analyze_word(u"sálvanos")
analyze_word(u"acercaros")
analyze_word(u' ')
analyze_word(u"trabajo")
analyze_word(u"burros")
analyze_word(u"majos")
analyze_word(u"mala")
analyze_word(u"las")
analyze_word(u"verde")
analyze_word(u"kjlkj;")
analyze_word(u"hkjhtela")

print(u'Escribe tu palabra aquí.'
      u'Si no quieres seguir, escribe QUIT.')

while True:
  my_word = input(u'>>> ')
  my_word = u"{}".format(my_word)
  if my_word.upper() == 'QUIT':
    sys.exit()
  else:
    analyze_word(my_word)

