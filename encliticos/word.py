#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from .form import VerbalForm
from .structure import Structure


class Word:

  PRONOUNS =  'lo|la|los|las|se|le|les|nos|os|me|te'

  PATTERN =  re.compile(r'(^\w+?)(?:({}))?(?:({}))?(?:({}))?$'.format(PRONOUNS, PRONOUNS, PRONOUNS))

  TILDED = [u'á', u'ú', u'í', u'é', u'ó']
  TILDLESS = [u'a', u'u', u'i', u'e', u'o']

  LAST_LETTER = {
    u'os': {
      'length': 1,
      'last_letters': [u'a', u'e', u'í', u'i'],
      'add_letter': u'd'
    },
    u'nos': {
      'length': 2,
      'last_letters': [u'mo'],
      'add_letter': u's'
    },
    u'se': {
      'length': 2,
      'last_letters': [u'mo'],
      'add_letter': u's'
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
    self.stressless = word
    self.structures = []
    self.current_base = None
    self.current_enclitics = None

  def swap_stress(self, word, keys, values):
    stresses = dict(zip(keys, values))
    new_word = word
    for key, value in stresses.items():
      if key in word:
        new_word = word.replace(key, value)
    return new_word

  def add_letter(self):
    #gets the correct verbal form of vámonos, démosela, tomaos:
    #TODO improve try/except
    #TODO do we need these two blocks?
    try:
      encl = self.current_enclitics[0]
    except IndexError:
      return has_extra_letter
    try:
      encl_dict = self.LAST_LETTER[encl]
    except KeyError:
      return has_extra_letter
             
    pos = encl_dict['length']
    if len(self.current_base) > pos:
      if self.current_base[-pos:] in encl_dict['last_letters']:
        self.current_base += encl_dict['add_letter']
        
  def encl_to_base(self):
    self.current_base = self.current_base + self.current_enclitics[0]     
    self.current_enclitics = self.current_enclitics[1:]

  def get_structures(self):
    structures = self.detect_verbs()
    want_more_structures = False
    if structures:
      for structure in structures:
        self.structures.append(structure)
        if self.current_enclitics:
          #TODO: modify combination None, change order
          if not structure.valid or structure.has_extra_letter or (
          structure.combination and structure.combination.error):
              want_more_structures = True
    else:
      if self.current_enclitics:
        want_more_structures = True            
    if want_more_structures:
      self.encl_to_base()
      self.get_structures()

  def detect_verbs(self):
    if self.current_enclitics:
      if self.current_enclitics[0] in ['nos', 'se', 'os']:
        self.add_letter()
    structures, iig_structures = self.build_structures(self.current_base)
    if not structures:
      letters = list(self.current_base)
      for index, letter in enumerate(letters):
        if letter in self.TILDLESS:
          stressed_letter = self.swap_stress(letter, self.TILDLESS, self.TILDED)
          new_letters = letters[:]
          new_letters[index] = stressed_letter
          structures, iig_structures = self.build_structures(''.join(new_letters))
          if structures:
            break
    if iig_structures:
      structures = iig_structures
    return structures     

  def build_structures(self, verb):
    lemmas = self.APICULTUR.lematiza2(word=verb)['lemas']
    structures = []
    iig_structures = []
    for lemma in lemmas:
      try:
        new_form = VerbalForm(lemma)
      except ValueError:
        None
      else:
        word = self.word[:]
        encls = self.current_enclitics[:]
        new_structure = Structure(word, new_form, encls)
        structures.append(new_structure)
        if new_structure.valid:
          iig_structures.append(new_structure)
    return structures, iig_structures

  def get_enclitics(self):
    self.stressless = self.swap_stress(self.word, self.TILDED, self.TILDLESS)
    base_encl = self.PATTERN.search(self.stressless).groups()
    self.current_base = base_encl[0]
    # self.current_enclitics = base_encl[1:]
    self.current_enclitics = [value for value in base_encl[1:] if value != None]

  def analyze_word(self):
    self.get_enclitics()
    self.get_structures()
    #TODO delete repetition for bailamostelo
    new_structures = list(set(self.structures))
    self.structures = new_structures


        # if self.word != self.accentuated:
        #   print(u'\t\t¿Estás seguro de no haberte equivocado '
        #         u'con los acentos? ¿Quizá quisiste decir "{}"?'
        #         .format(self.accentuated))  




