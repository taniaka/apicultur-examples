#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:

    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from structure import Structure

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
      'os': 'directo o indirecto',
      'te': 'directo o indirecto',
      'se': 'indirecto, sustituyendo a "le" o "les"'
  }

  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  def __init__(self, word):
    self.word = word
    self.structures = []

  def get_last(self, word, num):
    last_syls = []
    syllabized = self.APICULTUR.silabeame(word=word)
    syllables = syllabized['palabraSilabeada'].split('=')
    for syl in range(num):
      index = -(syl+1)
      try:
        last_syls.insert(0,syllables[index])
      except:
        break              
    return last_syls

  def del_accent(self, my_word):
    accentless = my_word
    accents = {u'á': 'a', u'ú':'u', u'í':'i', u'é':'e', u'ó':'o'}
    last_two = self.get_last(my_word, 2)
    if my_word[-1] in ['r', 'd']:
      syllable = last_two[-1]
    else:
      syllable = last_two[0]
    for key, value in accents.items():
      if key in syllable:
        new_syllable = syllable.replace(key, value)
        accentless = my_word.replace(syllable, new_syllable)    
        break
    return accentless   

  def add_letter(self, base_word, encl):
    #detect vámonos and démosela types of verbs      
    pos_1 = self.word.rfind(encl)
    pos_2 = self.word.rfind('mo'+encl)
    if pos_1 == pos_2 + 2:
      if pos_2 not in [0, 1]:
        base_word = base_word + 's'
    return base_word    

  def get_enclitics(self, syls):
    second_last, last = syls[0], syls[1]
    base_word = self.word
    enclitics = []
    if last in self.PRONOUNS:
      enclitics.append(last)
      if second_last in self.PRONOUNS:
        enclitics.insert(0,second_last)
    if len(enclitics) < 2:
      #caso 'tomárosla'
      if second_last in ['dos', 'ros']:
        enclitics = ['os', last]
      #casos 'tomaros', 'plumeros', 'tomados', volver a detectar
      elif last in ['dos', 'ros']:
        second_last += last[0]
        return self.get_enclitics([second_last, 'os'])
      #caso 'tomárosos'
      elif second_last in ['do', 'ro'] and last == 'sos':
        enclitics = ['os', 'os']
    if ''.join(enclitics) == self.word:
      base_word = second_last
      enclitics = [last]
    else:
      if enclitics:
        length = len(''.join(enclitics))
        base_word = self.word[0:-length]
        if enclitics[0] in ['nos', 'se']:
          base_word = self.add_letter(base_word, enclitics[0])
    base_word = self.del_accent(base_word)
    return base_word, enclitics

  def is_regular(self, part, base_word):
    #mark vámosnos, démossela y marchados as invalid for enclitics
    #TODO disambiguate marchados
    parts = {'mos': ['nos', 'se'], 'd': ['os']}
    try:
      encls = parts[part]
    except:
      return True  
    for encl in encls:
      if self.word.rfind(part+encl) != -1:
        return False
    return True 
  

  def detect_verbs(self, base_word, enclitics):
    iig_infinitives = [] #infinitives for inf, imp and ger forms
    infinitives = []
    is_valid_form = False
    lemmas = self.APICULTUR.lematiza2(word=base_word)
    if lemmas:
      for lemma in lemmas['lemas']:
        category = lemma['categoria']
        if category[0] == 'V':
          infinitives.append(lemma['lema'])
          if category[0:3] in ['VMM', 'VMG', 'VMN']:
            is_valid_form = True
            iig_infinitives.append(lemma['lema'])
            
            # print(base_word, enclitics, is_valid_form, infinitives)
            if base_word != self.word and infinitives:
              if base_word[-3:] == 'mos':
                is_valid_form = self.is_regular('mos', base_word)
              elif base_word[-1:] == 'd':
                is_valid_form = self.is_regular('d', base_word)

              if iig_infinitives:       
                infinitives = iig_infinitives
    
    infinitives = list(set(infinitives))
    # True, infinitives => this is a valid verbal form that can take enclitics
    # False, infinitives => this is a verbal form but it can't take enclitics
    # False, no infinitives => this is not a verbal form
    return is_valid_form, infinitives

  def modify_structure(self, base_word, enclitics):
    new_base_word = base_word + enclitics[0]     
    new_enclitics = enclitics[1:]
    return self.get_structure(new_base_word, new_enclitics)  

  def get_structure(self, base_word, enclitics):
    is_valid_form, infinitives = self.detect_verbs(base_word, enclitics)
    if not infinitives:
      if not enclitics:
        return
      else: 
        self.modify_structure(base_word, enclitics)

    else:
      structure = Structure(is_valid_form, infinitives, enclitics)
      self.structures.append(structure)
      if enclitics and (not is_valid_form or
      not structure.valid_comb):
        self.modify_structure(base_word, enclitics)
    return      

  def analyze_word(self):
    #TODO: idos, comeros, comenos, comemos                
    print(u'Tu palabra es: {}.'.format(self.word.upper()))
    last_syls = self.get_last(self.word, 2)   
    if len(last_syls) == 1:
      print(u'\tTu palabra solo tiene una sílaba '
            u'y no puede tener enclíticos, intenta con otra palabra.')
      return

    base_word, enclitics = self.get_enclitics(last_syls)
    self.get_structure(base_word, enclitics)

    self.print_results()
    return

  def print_results(self):
    if not self.structures:
      print(u'\tParece que "{}" no es un verbo.'.
            format(self.word))
    else:
      for num, structure in enumerate(self.structures):       
        if len(self.structures) > 1:        
          print(u'Opción {}.'.format(num+1))
        elements = [(self.PRONOUNS[encl], encl) for encl in structure.enclitics]
        elements = [item for element in elements for item in element]
        print(structure.message.format(', '
        .join(structure.infinitives), *elements))
    return    


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
validate_word(u'dámosela')
validate_word(u'dámossela')
validate_word(u'acercaos')
validate_word(u'acercados')
validate_word(u'comedos')
validate_word(u'dime')
validate_word(u'seguirle')
validate_word(u'rompiéndonos')
validate_word(u'fíjate')
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
validate_word(u'cenan')
validate_word(u'dfghdfhfghmela')
validate_word(u'majos')
validate_word(u'mala')
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

