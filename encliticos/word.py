#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from .structure import Structure

class Word:

  PRONOUNS =  ['la', 'las', 'le', 'les', 'lo','los',
               'nos', 'me', 'os', 'te', 'se']

  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  def __init__(self, word):
    self.word = word
    self.syllables = self.syllabize()
    self.structures = []


  def syllabize(self):
    syllabized = self.APICULTUR.silabeame(word=self.word)
    syls = syllabized['palabraSilabeada'].split('=')
    if len(syls) > 1:
      if set([syls[-2], syls[-1]]).intersection(
                                  ['dos', 'ros', 'do', 'ro']):
        syls = self.modify_syllables(syls)
    return syls

  def modify_syllables(self, syls):
    prelast, last = syls[-2], syls[-1]
    #casos 'tomaros', 'plumeros', 'tomados'
    if last in ['dos', 'ros']:
      syls[-2] += last[0]
      syls[-1] = 'os'
    else:
      if len(syls) >= 3:  
        #caso 'tomárosla'
        if prelast in ['dos', 'ros']:
          syls[-3] += prelast[0]
          syls[-2] = 'os'
        #caso 'tomárosos'
        elif prelast in ['do', 'ro'] and last == 'sos':
          syls[-3] += prelast[0]
          syls[-2], syls[-1] = 'os', 'os'
    return syls

    
    #       #TODO remove repetition
    #       if base_word != self.word and infinitives:
    #         if base_word[-3:] == 'mos':
    #           regular = self.is_regular('mos', base_word)
    #         elif base_word[-1:] == 'd':
    #           regular = self.is_regular('d', base_word)

   
  def swap_stress(self, word, keys, values):
    stresses = dict(zip(keys, values))
    new_word = word  
    for key, value in stresses.items():
      if key in word:
        new_word = word.replace(key, value)
    return new_word      

  def del_stress(self, base_word, enclitics):
    stressed_vocs = [u'á', u'ú', u'í', u'é', u'ó']
    unstressed_vocs = [u'a', u'u', u'i', u'e', u'o']   
    stressless = self.swap_stress(base_word, stressed_vocs, unstressed_vocs)
    return stressless

  def add_to_base(self, base_word, encl):
    #gets the correct verbal form of vámonos, démosela, tomaos:
    # 'vámos', 'démos', 'tomad'  
    #TODO error if wrong enclitic is passed
    pairs = {'os': [1, ['a', 'e', 'í', 'i'], 'd'],
            'nos': [2, ['mo'], 's'],
            'se':  [2, ['mo'], 's']
    }
    pos = pairs[encl][0]
    if len(base_word) > pos:
      if base_word[-pos:] in pairs[encl][1]:
        base_word += pairs[encl][2]
    return base_word

  def verbs_in_lemas(self, lemmas):
    if lemmas:
      lemas = []
      for lemma in lemmas:
        category = lemma['categoria']
        if category[0] == 'V':
          lemas.append(lemma)
    return lemas

  def detect_verbs(self, base_word, enclitics):
    if enclitics:
      #BASE_WORD STEP 2 (get base with correct verbal form)
      if enclitics[0] in ['nos', 'se', 'os']:
        base_word = self.add_to_base(base_word, enclitics[0])
    if base_word == 'esta':
      base_word = 'está'
    elif base_word == 'este':
      base_word = 'esté'
    lemmas = self.APICULTUR.lematiza2(word=base_word)['lemas']
    lemas = self.verbs_in_lemas(lemmas)
    if not lemas:
      #BASE_WORD STEP 3 (get base with correct stress)
      stressless = self.del_stress(base_word, enclitics) 
      lemmas = self.APICULTUR.lematiza2(word=stressless)['lemas']
      lemas = self.verbs_in_lemas(lemmas)    
    return lemas

  def modify_structure(self, base_word, enclitics):
    new_base_word = base_word + enclitics[0]     
    new_enclitics = enclitics[1:]
    return new_base_word, new_enclitics 

  def get_structure(self, base_word, enclitics):
    lemas = self.detect_verbs(base_word, enclitics)
    if not lemas:
      if not enclitics:
        return
      else:
        new_base_word, new_enclitics = self.modify_structure(base_word, enclitics)
        self.get_structure(new_base_word, new_enclitics)          
    #TODO get the original base_word
    else:
      structure = Structure(lemas, enclitics)
      #TODO si la nueva estructura es correcta, eliminar la anterior
      self.structures.append(structure)
      if enclitics:
       if not structure.valid or (structure.type == 'combination' and
       not structure.combination.is_valid):
          new_base_word, new_enclitics = self.modify_structure(base_word, enclitics)
          self.get_structure(new_base_word, new_enclitics)                

  def get_enclitics(self, second_last, last):
    base_word = self.word
    enclitics = []
    length = len(self.syllables)
    if last in self.PRONOUNS:
      enclitics.append(last)
      if length > 2:
        if second_last in self.PRONOUNS:
          enclitics.insert(0,second_last)

    if enclitics:
      base_syls = self.syllables[:-len(enclitics)]
      #BASE_WORD STEP 1 (original base)
      base_word = ''.join(base_syls)
    return base_word, enclitics


  def analyze_word(self):
    print(u'\nTu palabra es: {}.'.format(self.word.upper()))

    if len(self.syllables) < 2:
      print(u'\tTu palabra solo tiene una sílaba y no puede'
            u'tener enclíticos, intenta con otra palabra.')
      return
    prelast, last = self.syllables[-2], self.syllables[-1]
    base_word, enclitics = self.get_enclitics(prelast, last)
    self.get_structure(base_word, enclitics)
    self.print_results()

  def print_results(self):
    if not self.structures:
      print(u'\tParece que "{}" no es un verbo.'.
            format(self.word))
    else:
      for num, structure in enumerate(self.structures):       
        if len(self.structures) > 1:        
          print(u'Opción {}.'.format(num+1))
        structure.print_message()
        # if self.word != self.accentuated:
        #   print(u'\t\t¿Estás seguro de no haberte equivocado '
        #         u'con los acentos? ¿Quizá quisiste decir "{}"?'
        #         .format(self.accentuated))  




