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

  TILDED = [u'á', u'ú', u'í', u'é', u'ó']
  TILDLESS = [u'a', u'u', u'i', u'e', u'o']

  EXTRA_LETTERS = {
    u'os': {
      'length': 1,
      'last_letters': [u'a', u'e', u'í', u'i'],
      'add_letter': u'd',
      'bad_end': u'd'
    },
    u'nos': {
      'length': 2,
      'last_letters': [u'a', u'e', u'í', u'i'],
      'add_letter': u'd',
      'bad_end': u'd',
    },
    u'se': {
      'length': 2,
      'last_letters': [u'a', u'e', u'í', u'i'],
      'add_letter': u'd',
      'bad_end': u'd'
    }
  }

  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  def __init__(self, word):
    word.strip()
    try:
      assert word.isalpha()
    except AssertionError:
      raise ValueError(u'Parece que no es una palabra. Vuelve a intentar.\n')
    self.word = word
    self.syllables = self.syllabicate()
    self.structures = []
    # self.analyze_word()


  def syllabicate(self):
    syllabicated = self.APICULTUR.silabeame(word=self.word)
    syls = syllabicated['palabraSilabeada'].split('=')
    length = len(syls)
    if length > 1:  
      syls = self.modify_syllables(syls)
    return syls

  def modify_syllables(self, syls):
    num = 3
    if len(syls) == 2:
      num = 2
    for n in range(num):
      i = -(n+1)
      #casos 'tomaros','tomárosla','tomárosmela'
      if syls[i] in ['dos', 'ros']:
        try:
          syls[i-1] += syls[i][0]
        except IndexError:
          pass
        else:  
          syls[i] = 'os'
      #casos'tomárosos', 'tomárososla'
      elif syls[i] == 'sos':
        if (1-i) < len(syls) and syls[i-1] in ['do', 'ro']:
          syls[i-2] += syls[i-1][0]
          syls[i-1], syls[i] = 'os', 'os'

    return syls


  def swap_stress(self, word, keys, values):
    stresses = dict(zip(keys, values))
    new_word = word  
    for key, value in stresses.items():
      if key in word:
        new_word = word.replace(key, value)
    return new_word      

  def add_to_base(self, base_word, encls):
    #gets the correct verbal form of vámonos, démosela, tomaos:
    # 'vámos', 'démos', 'tomad'
    #TODO reorganize dict?
    encl = encls[0]
    encl_dict = self.EXTRA_LETTERS[encl]
    is_regular = True
    bad_end = encl_dict['bad_end']
    bad_ending = bad_end + ''.join(encls)
    ending_pos  = self.word.rfind(bad_ending)

    if ending_pos != -1:
      if (len(self.word) - ending_pos) == len(bad_ending):
        if self.word != 'idos':
          is_regular = False
    else:
      pos = encl_dict['length']
      if len(base_word) > pos:
        if base_word[-pos:] in encl_dict['last_letters']:
          base_word += encl_dict['add_letter']
    return is_regular, base_word

  def verbs_in_lemas(self, lemmas):
    if lemmas:
      lemas = []
      for lemma in lemmas:
        category = lemma['categoria']
        if category[0] == 'V':
          lemas.append(lemma)
    return lemas

  def detect_verbs(self, base_word, enclitics):
    is_regular = True
    if enclitics:
      #BASE_WORD STEP 2 (get base with correct verbal form)
      if enclitics[0] in ['nos', 'se', 'os']:
        is_regular, base_word = self.add_to_base(base_word, enclitics)

    #BASE_WORD STEP 3 (get base with correct stress)
    stressless = self.swap_stress(base_word, self.TILDED, self.TILDLESS) 
    lemmas = self.APICULTUR.lematiza2(word=stressless)['lemas']
    lemas = self.verbs_in_lemas(lemmas)
    if not lemas:
      #can't use the syllabicated word because of the diphtongs
      letters = list(stressless)
      start = 0
      for index, letter in enumerate(letters):
        if letter in self.TILDLESS:
          syl = ''.join(letters[start:index+1])
          stressed_syl = self.swap_stress(syl, self.TILDLESS, self.TILDED)
          #TODO avoid replacing twice
          restressed = stressless.replace(syl, stressed_syl)
          lemmas = self.APICULTUR.lematiza2(word=restressed)['lemas']
          lemas = self.verbs_in_lemas(lemmas)
          start = index + 1
          if lemas:
            break  
    return is_regular, lemas

  def modify_structure(self, base_word, enclitics):
    new_base_word = base_word + enclitics[0]     
    new_enclitics = enclitics[1:]
    return new_base_word, new_enclitics 

  def get_structure(self, base_word, enclitics):
    is_regular, lemas = self.detect_verbs(base_word, enclitics)
    if not lemas:
      if not enclitics:
        return
      else:
        new_base_word, new_enclitics = self.modify_structure(base_word, enclitics)
        self.get_structure(new_base_word, new_enclitics)          
    #TODO get the original base_word
    else:
      structure = Structure(is_regular, lemas, enclitics)
      #TODO si la nueva estructura es correcta, eliminar la anterior
      self.structures.append(structure)
      if enclitics:
       if not structure.valid or (len(enclitics) >= 2 and
        structure.combination.error):
          new_base_word, new_enclitics = self.modify_structure(base_word, enclitics)
          self.get_structure(new_base_word, new_enclitics)                

  def get_enclitics(self):
    base_word = self.word
    enclitics = []
    prelast, last = self.syllables[-2], self.syllables[-1]
    length = len(self.syllables)
    #TODO shorten?
    if last in self.PRONOUNS:
      enclitics.append(last)
      if length > 2:
        if prelast in self.PRONOUNS:
          enclitics.insert(0, prelast)
          if length > 3:
            preprelast = self.syllables[-3]
            if preprelast in self.PRONOUNS:
              enclitics.insert(0, preprelast)

    if enclitics:
      base_syls = self.syllables[:-len(enclitics)]
      #BASE_WORD STEP 1 (original base)
      base_word = ''.join(base_syls)
    return base_word, enclitics


  def analyze_word(self):
    try:
      base_word, enclitics = self.get_enclitics()
    except IndexError:
      raise ValueError(u'\tTu palabra solo tiene una sílaba y no puede'
                       u'tener enclíticos, intenta con otra palabra.')
    self.get_structure(base_word, enclitics)


        # if self.word != self.accentuated:
        #   print(u'\t\t¿Estás seguro de no haberte equivocado '
        #         u'con los acentos? ¿Quizá quisiste decir "{}"?'
        #         .format(self.accentuated))  




