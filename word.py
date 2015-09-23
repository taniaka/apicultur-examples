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
    self.accentuated = self.word

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

  def change_accent(self, syl, word, keys, values):
    accents = dict(zip(keys, values))
    new_word = word  
    for key, value in accents.items():
      if key in syl:
        new_syllable = syl.replace(key, value)
        new_word = word.replace(syl, new_syllable)
        break
    return new_word      

  def del_accent(self, base_word, enclitics):
    with_acc = [u'á', u'ú', u'í', u'é', u'ó']
    no_acc = [u'a', u'u', u'i', u'e', u'o']
    accentless = base_word
    syllable =''
    #TODO remove repetition
    if base_word == u'esta' or base_word == u'está':
      accentless = u'está'
      if base_word == u'está':
        self.accentuated = u'esta'
        self.accentuated += ''.join(enclitics)
    elif base_word == u'este' or base_word == u'esté':
      accentless = u'esté'
      if base_word == u'esté':
        self.accentuated = u'este'
        self.accentuated += ''.join(enclitics)
    elif base_word[-1] == 'a' and enclitics[0] == 'os':
      self.accentless = base_word
    else:
      last_two = self.get_last(base_word, 2)
      if len(last_two) > 1 or len(enclitics) > 1:    
        if base_word[-1] in ['r', 'd']:
         if len(enclitics) > 1:
          syllable = last_two[-1]
        else:
          syllable = last_two[0]
          
        if syllable:
          accentless = self.change_accent(syllable, base_word, 
          with_acc, no_acc)
        if accentless == base_word:
          self.accentuated = self.change_accent(syllable, base_word, 
            no_acc, with_acc)
          self.accentuated += ''.join(enclitics)

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

    encl_string = ''.join(enclitics)
    if encl_string == self.word:
      base_word = second_last
      enclitics = [last]
    else:
      if enclitics:
        length = len(encl_string)
        base_word = self.word[0:-length]
        if enclitics[0] in ['nos', 'se']:
          base_word = self.add_letter(base_word, enclitics[0])
        base_word = self.del_accent(base_word, enclitics)
    return base_word, enclitics

  def is_regular(self, part, base_word):
    #mark vámosnos, démossela y marchados as irregular form
    #TODO disambiguate marchados
    parts = {'mos': ['nos', 'se'], 'd': ['os']}
    try:
      encls = parts[part]
    except:
      return True
    for encl in encls:
      if self.word.rfind(part+encl) != -1 and self.word != 'idos':
        return False
    return True 
  
  def is_reflexive(self, v_pers, v_num, enclitics):
    first = enclitics[0]
    length = len(enclitics)
    pr_pers, pr_num = None, None

    if first == 'se':
      if length == 1:
        return (True, True)
      elif length == 2:
        second = enclitics[1]
        if not pr_pers:
          if second in ['la', 'lo', 'las', 'los']:
            return (True, False)
          else:
            return (True, True)
        else:
          if pr_pers == 3:
            return (True, False)
        #TODO mark acerquémosele as invalid combination.    

    elif first in ['me', 'te', 'nos', 'os']:
      if not v_pers and not v_num:
        return (True, False)
      else:
        pr_lemas = self.APICULTUR.lematiza2(word=first)['lemas']
        for pr_lema in pr_lemas:
          pr_cat = pr_lema['categoria']
          if pr_cat[:2] == 'PP':
            pr_pers, pr_num = pr_cat[2], pr_cat[4]
            break
        if pr_pers == v_pers and pr_num == v_num:
          return (True, True)
        elif v_pers == '2' and v_num == 'S' and first == 'os':
          return(True, True)  
    #return (can it be reflexive, is it always reflexive)
    return (False, False)


  def detect_verbs(self, base_word, enclitics):
    iig_infinitives = [] #infinitives for inf, imp and ger forms
    infinitives = []
    is_valid_form = False
    regular = True
    reflexive = (False, False)
    v_pers, v_num = None, None
    lemmas = self.APICULTUR.lematiza2(word=base_word)
    if lemmas:
      for lemma in lemmas['lemas']:
        category = lemma['categoria']
        if category[0] == 'V':
          infinitives.append(lemma['lema'])

          if category[0:3] in ['VMM', 'VMG', 'VMN', 
                              'VAM', 'VAG', 'VAN']:
            is_valid_form = True
            iig_infinitives.append(lemma['lema'])
            if enclitics:
              if category[0:3] == 'VMM':
                v_pers, v_num = category[4], category[5]
              reflexive = self.is_reflexive(v_pers, v_num, enclitics)
            
          #TODO remove repetition
          if base_word != self.word and infinitives:
            if base_word[-3:] == 'mos':
              regular = self.is_regular('mos', base_word)
            elif base_word[-1:] == 'd':
              regular = self.is_regular('d', base_word)

          if iig_infinitives:       
            infinitives = iig_infinitives[:]
    
          infinitives = list(set(infinitives))

    # True, True <= pregúntaselo, démoselo
    # False, True <= doytelo, dámoselo
    # False, False <= dámosselo
    # True, False <= démosselo
    # No infinitives <= not a verbal form
    return is_valid_form, regular, reflexive, infinitives

  def modify_structure(self, base_word, enclitics):
    new_base_word = base_word + enclitics[0]     
    new_enclitics = enclitics[1:]
    return self.get_structure(new_base_word, new_enclitics)  

  def get_structure(self, base_word, enclitics):
    is_valid_form, is_regular, reflexive, infinitives = self.detect_verbs(
                                                        base_word, enclitics)
    if not infinitives:
      if not enclitics:
        return
      else: 
        self.modify_structure(base_word, enclitics)

    else:
      structure = Structure(is_valid_form, is_regular, 
                  reflexive, infinitives, enclitics)
      #TODO si la nueva estructura es correcta, eliminar la anterior
      self.structures.append(structure)
      if enclitics:
       if not is_valid_form or (structure.type == 'combination' and
       not structure.combination.is_valid):
        self.modify_structure(base_word, enclitics)    

  def analyze_word(self):
    print(u'\nTu palabra es: {}.'.format(self.word.upper()))
    last_syls = self.get_last(self.word, 2)   
    if len(last_syls) == 1:
      print(u'\tTu palabra solo tiene una sílaba '
            u'y no puede tener enclíticos, intenta con otra palabra.')
      return

    base_word, enclitics = self.get_enclitics(last_syls)
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
        print(structure.message)
        if self.word != self.accentuated:
          print(u'\t\t¿Estás seguro de no haberte equivocado '
                u'con los acentos? ¿Quizá quisiste decir "{}"?'
                .format(self.accentuated))  



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
validate_word(u'démosela')
validate_word(u'dámossela')
validate_word(u'acercaos')
validate_word(u'acercados')
validate_word(u'comedos')
validate_word(u'acercarselo')
validate_word(u'acercársele')
validate_word(u'acercasela')
validate_word(u'acérquensela')
validate_word(u'acérquensele')
validate_word(u"estate")
validate_word(u"estáte")
validate_word(u'dime')
validate_word(u'idos')
validate_word(u'seguirle')
validate_word(u'rompiéndonos')
validate_word(u'rompiendonos')
validate_word(u'fíjate')
validate_word(u'fijate')
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
validate_word(u'dfghdfhfghmela')
validate_word(u'majos')
validate_word(u'mala')
validate_word(u'verde')
validate_word(u'las')
validate_word(u'123')
validate_word(u'dame1la')
validate_word(u' ')
validate_word(u'')


print(u'\nEscribe tu palabra aquí.'
      u'Si no quieres seguir, escribe QUIT.')

while True:
  word = input(u'>>> ')
  word = u"{}".format(word)
  print(word)
  if word.upper() == u'QUIT':
    sys.exit()
  else:
    validate_word(word)

