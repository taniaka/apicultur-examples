#!/usr/bin/env python
# -*- coding: utf-8 -*-

from combination import Combination

class Structure:

  STRUCTURE_TYPES = ('no_encl', 'unique_encl', 'combination')

  VERB_MESSAGES = {  
    True: u'\t\tTu forma verbal es un infinitivo, imperativo '\
          u'o gerundio, por lo tanto se puede usar con enclíticos.\n',

    False:  u'\tSin embargo, te advertimos que los enclíticos '
            u'deberían usarse solo con infinitivos, gerundios '
            u'e imperativos. En algunas regiones, por ejemplo '
            u'en Asturias, los pronombres pueden posponer al indicativo, condicional '
            u'y subjuntivo, pero en el castellano estándar está en desuso.\n'
  }

  ENC_MESSAGES = {
    'combination':  u'\tTienes dos enclíticos:\n'\
                    u'\t\tEl primero es un complemento {}: {}.\n'\
                    u'\t\tEl segundo es un complemento {}: {}.',

    'unique_encl': u'\tTienes un enclítico de tipo complemento {}: {}.',
    'no_encl': u'\tNo se han detectado enclíticos.'
  }

  def __init__(self, valid_form, infinitives, enclitics):
    self.valid_form = valid_form
    self.infinitives = infinitives
    self.enclitics = enclitics

    self.type = self.STRUCTURE_TYPES[len(enclitics)]
    self.combination = None
    self.valid_comb = True
    self.message = self.build_message()

  def build_message(self):
    message = u'\tTienes un verbo que puede ser uno de los siguientes: {}.\n'
    if self.type != 'no_encl':
      message +=  self.VERB_MESSAGES[self.valid_form]
 
    message += self.ENC_MESSAGES[self.type]
    if self.type == 'combination':
      combination = ''.join(self.enclitics)  
      self.combination = Combination(combination)
      self.valid_comb = self.combination.is_valid
      message += self.combination.message

    return message


