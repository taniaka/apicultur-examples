#!/usr/bin/env python
# -*- coding: utf-8 -*-

from combination import Combination

class Structure:

  STRUCTURE_TYPES = ('no_encl', 'one_encl', 'combination')

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
    'valid' : {  
      True : u'\t\tTu forma verbal es un infinitivo, imperativo '
             u'o gerundio, por lo tanto se puede usar con enclíticos.\n',
      False: u'\t\tSin embargo, te advertimos que los enclíticos '
             u'deberían usarse solo con infinitivos, gerundios '
             u'e imperativos. En algunas regiones, por ejemplo '
             u'en Asturias, los pronombres pueden posponer al indicativo, condicional '
             u'y subjuntivo, pero en el castellano estándar está en desuso.\n'
    },
    'regular' : {
      True : u'',
      False: u'\t Sin embargo...(explicar por qué vamosnos o demossela o tomados son incorrectos).\n'
    }
  }

  ENC_MESSAGES = {
    'combination':  u'\tTienes dos enclíticos:\n'\
                    u'\t\tEl primero es un {}: {}.\n'\
                    u'\t\tEl segundo es un {}: {}.',

    'one_encl': u'\tTienes un enclítico de tipo {}: {}.',
    'no_encl': u'\tNo se han detectado enclíticos.'
  }

  def __init__(self, valid, regular, reflexive, infinitives, enclitics):
    self.valid = valid
    self.regular = regular
    self.reflexive = reflexive
    self.infinitives = infinitives
    self.enclitics = enclitics

    self.type = self.STRUCTURE_TYPES[len(enclitics)]
    self.combination = None
    if self.type == 'combination':     
      self.combination = Combination(''.join(enclitics))
    self.message = self.build_message()          

  def build_message(self):
    message = u'\tTienes un verbo que puede ser uno de los siguientes: {}.\n'
    if self.type != 'no_encl':
      message += (self.VERB_MESSAGES['valid'][self.valid] +
                  self.VERB_MESSAGES['regular'][self.regular])
 
    message += self.ENC_MESSAGES[self.type]
    elms = [(self.PRONOUNS[encl], encl) for encl in self.enclitics]
    elms = [item for elm in elms for item in elm]
    if self.type == 'combination':     
      #if comb is valid, the 1st encl is indir and the 2nd one is dir
      if self.combination.is_valid and ''.join(self.enclitics) not in ['sele', 'seles']:
        elms[0] = u'complemento indirecto'
        elms[2] = u'complemento directo'
      message += self.combination.message

    if self.reflexive == (True, True):
      elms[0] = u'pronombre reflexivo (o impersonal, a ver cómo lo llamamos)'
    if self.reflexive == (True, False):
      elms[0] += u'. También puede ser un pronombre reflexivo'
    
    message = message.format(', '
      .join(self.infinitives), *elms)

    return message


