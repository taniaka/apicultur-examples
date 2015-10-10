#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)

from .combination import Combination
from .form import PersonalPronominalForm


class Structure:

  APICULTUR = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")

  PRONOUNS =  {
    'la':  'complemento directo',
    'las': 'complemento directo',
    'le':  'complemento indirecto',
    'les': 'complemento indirecto',
    'lo':  'complemento directo',
    'los': 'complemento directo',
    'nos': 'complemento directo o indirecto',
    'me':  'complemento directo o indirecto',
    'os':  'complemento directo o indirecto',
    'te':  'complemento directo o indirecto',
    'se':  'complemento indirecto, sustituyendo a "le" o "les"'
  }

  VERB_MESSAGES = {
    'valid': {  
      True : u'\t\tTu forma verbal es un infinitivo, imperativo '
             u'o gerundio, por lo tanto se puede usar con enclíticos.\n',
      False: u'\t\tSin embargo, te advertimos que los enclíticos '
             u'deberían usarse solo con infinitivos, gerundios '
             u'e imperativos. En algunas regiones, por ejemplo '
             u'en Asturias, los pronombres pueden posponer al indicativo, condicional '
             u'y subjuntivo, pero en el castellano estándar está en desuso.\n'
    },
    'extra_letter': {
      False : u'',
      True: u'\t Sin embargo...(explicar por qué vamosnos o demossela '
             u'o tomados son incorrectos).\n'
    }
  }

  ENC_MESSAGES = [u'\tNo se han detectado enclíticos.',

                  u'\tTienes un enclítico de tipo {}: {}.',

                  u'\tTienes dos enclíticos:\n'\
                  u'\t\tEl primero es un {}: {}.\n'\
                  u'\t\tEl segundo es un {}: {}.',

                  u'\tTienes tres enclíticos:\n'\
                  u'\t\tEl primero es un {}: {}.\n'\
                  u'\t\tEl segundo es un {}: {}.\n'
                  u'\t\tEl tercero es un {}: {}.'
  ]

  EXTRA_LETTER = {
    u'os': u'd',
    u'nos': u'mos',
    u'se': u'mos'
  }

  def __init__(self, word, form, enclitics):
    self.word = word
    self.form = form
    self.enclitics = enclitics
    self.has_extra_letter = self.has_extra_letter()
    self.valid = self.form.mode in ['M', 'N', 'G']

    self.reflexive = self.is_reflexive()

    #TODO: Create combination with none error and message
    self.combination = None
    if len(enclitics) >= 2:     
      self.combination = Combination(enclitics)
    self.message = self.build_message()

  #TODO: check if correct
  def __hash__(self):
    return 1

  def __eq__(self, other): 
    return self.__dict__ == other.__dict__

  def has_extra_letter(self):
    #checks if the verb is of vámosnos, démossela, tomados type:
    has_extra_letter = False
    try:
      encl = self.enclitics[0]
    except IndexError:
      return has_extra_letter

    try:
      bad_end = self.EXTRA_LETTER[encl]
    except KeyError:
      return has_extra_letter
    bad_ending = bad_end + ''.join(self.enclitics)
    ending_pos  = self.word.rfind(bad_ending)
    print(self.word, bad_ending, ending_pos)

    if (len(self.word) - ending_pos) == len(bad_ending) and ending_pos != -1:
      if self.word != 'idos':
        has_extra_letter = True
    return has_extra_letter

  def is_reflexive(self):
    can_be_reflexive = False
    always_reflexive = False
    try:
      first = self.enclitics[0]
    except IndexError:
      None
    else:
      length = len(self.enclitics)

      if first == 'se':
        try:
          second = self.enclitics[1]
        except IndexError:
          can_be_reflexive, always_reflexive = True, True
        else:
          if length == 2:
            if self.form.mode in ['N', 'G', 'P']:
              can_be_reflexive = True
              if second not in ['la', 'lo', 'las', 'los']:
                always_reflexive = True
            else:
              if self.form.person == '3':
                can_be_reflexive = True
          else:
            can_be_reflexive, always_reflexive = True, True
                
      elif first in ['me', 'te', 'nos', 'os'] and length < 3:
        if self.form.mode in ['N', 'G', 'P']:
          can_be_reflexive = True
        else:
          pron_lemmas = self.APICULTUR.lematiza2(word=first)['lemas']
          for pron_lemma in pron_lemmas:
            try:
              pron_form = PersonalPronominalForm(pron_lemma)
            except ValueError:
              continue
            else:
              if (pron_form.person == self.form.person 
              and pron_form.number == self.form.number):
                can_be_reflexive, always_reflexive = True, True

    return (can_be_reflexive, always_reflexive)


  def build_message(self):
    length = len(self.enclitics)
    message = u'\tTienes un verbo: {}.\n'
    if length >= 1:
      message += (self.VERB_MESSAGES['valid'][self.valid]
              + self.VERB_MESSAGES['extra_letter'][self.has_extra_letter])
 
    message += self.ENC_MESSAGES[length]
    elms = [(self.PRONOUNS[encl], encl) for encl in self.enclitics]
    elms = [item for elm in elms for item in elm]
    if length >= 2:     
      #if comb is valid, 1st encl is indir and 2nd one is dir
      if (not self.combination.error and 
                ''.join(self.enclitics) not in ['sele', 'seles']):
        elms[-4] = u'complemento indirecto'
        elms[-2] = u'complemento directo'
      if length == 3 and self.enclitics[0] == 'se':
        elms[0] = 'pronombre reflexivo '  

      message += self.combination.message

    if self.reflexive == (True, True):
      elms[0] = u'pronombre reflexivo (o impersonal, a ver cómo lo llamamos)'
    if self.reflexive == (True, False):
      elms[0] += u'. También puede ser un pronombre reflexivo'
    
    return message.format(self.form.lemma, *elms)


