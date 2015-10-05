#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from .form import VerbalForm
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
      'last_letters': [u'mo'],
      'add_letter': u's',
      'bad_end': u'mos',
    },
    u'se': {
      'length': 2,
      'last_letters': [u'mo'],
      'add_letter': u's',
      'bad_end': u'mos'
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
    self.current_base = None
    self.current_enclitics = None

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

  def check_extra_letter(self):
    #gets the correct verbal form of vámonos, démosela, tomaos:
    # 'vámos', 'démos', 'tomad'
    has_extra_letter = False
    #TODO improve try/except
    try:
      encl = self.current_enclitics[0]
    except IndexError:
      return has_extra_letter

    try:
      encl_dict = self.EXTRA_LETTERS[encl]
    except KeyError:
      return has_extra_letter
             
    bad_end = encl_dict['bad_end']
    bad_ending = bad_end + ''.join(self.current_enclitics)
    ending_pos  = self.word.rfind(bad_ending)

    if ending_pos != -1:
      if (len(self.word) - ending_pos) == len(bad_ending):
        if self.word != 'idos':
          has_extra_letter = True
    else:
      pos = encl_dict['length']
      if len(self.current_base) > pos:
        if self.current_base[-pos:] in encl_dict['last_letters']:
          self.current_base += encl_dict['add_letter']
    return has_extra_letter
        
  def encl_to_base(self):
    self.current_base = self.current_base + self.current_enclitics[0]     
    self.current_enclitics = self.current_enclitics[1:]

  def get_structures(self):
    has_extra_letter, lemmas = self.detect_verbs()
    encls = self.current_enclitics
    structures = []
    #iig = infinitivo, gerundio, imperativo
    iig_structures = []
    for lemma in lemmas:
      try:
        new_form = VerbalForm(lemma)
      except ValueError:
        None
      else:
        new_structure = Structure(has_extra_letter, new_form, encls)
        structures.append(new_structure)
        if new_structure.valid:
          iig_structures.append(new_structure)

    want_more_structures = False

    if structures:
      if iig_structures:
        structures = iig_structures
      for structure in structures:
        self.structures.append(structure)
        if self.current_enclitics:
          #TODO: modify combination None, change order
          if not structure.valid or structure.extra_letter or (
          structure.combination and structure.combination.error):
              want_more_structures = True
    else:
      if self.current_enclitics:
        want_more_structures = True
            
    if want_more_structures:
      self.encl_to_base()
      self.get_structures()


  def detect_verbs(self):
    has_extra_letter = False
    if self.current_enclitics:
      #BASE_WORD STEP 2 (get base with correct verbal form)
      if self.current_enclitics[0] in ['nos', 'se', 'os']:
        has_extra_letter = self.check_extra_letter()
    #BASE_WORD STEP 3 (get base with correct stress)
    current_base = self.current_base
    stressless = self.swap_stress(current_base, self.TILDED, self.TILDLESS) 
    lemmas = self.APICULTUR.lematiza2(word=stressless)['lemas']

    if len(lemmas) == 1 and lemmas[0]['categoria'] == '0':
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
          start = index + 1
          if lemmas[0]['categoria'] != '0':
            break  
    return has_extra_letter, lemmas

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
    
    self.current_base = base_word
    self.current_enclitics = enclitics

  def analyze_word(self):
    try:
      self.get_enclitics()
    except IndexError:
      raise ValueError(u'\tTu palabra solo tiene una sílaba y no puede'
                       u'tener enclíticos, intenta con otra palabra.')
    self.get_structures()
    new_structures = list(set(self.structures))
    self.structures = new_structures
    # print(self.structures[0] == self.structures[1])


        # if self.word != self.accentuated:
        #   print(u'\t\t¿Estás seguro de no haberte equivocado '
        #         u'con los acentos? ¿Quizá quisiste decir "{}"?'
        #         .format(self.accentuated))  




