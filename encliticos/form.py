#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Form():
  def __init__(self, form, speech_part):
    self.lemma = form['lema']
    category = form['categoria']
    try:
      assert category[0] == speech_part
    except AssertionError:
      raise ValueError

  #TODO: check if correct?
  def __hash__(self):
    return 1      

  def __eq__(self, other): 
    return self.__dict__ == other.__dict__    


class VerbalForm(Form):
  def __init__(self, form):
    Form.__init__(self, form, 'V')
    #TODO get category from parent?
    category = form['categoria']
    self.mode = category[2]
    self.person = category[4]
    self.number = category[5]


class PronominalForm(Form):
  def __init__(self, form, pr_type):
    Form.__init__(self, form, 'P')
    category = form['categoria']
    try:
      assert category[1] == pr_type
    except AssertionError:
      raise ValueError
    else:
      self.person = category[2]
      self.number = category[4]


class PersonalPronominalForm(PronominalForm):
  def __init__(self, form):
    PronominalForm.__init__(self, form, 'P')








