#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Combination:

  VALID_COMBINATIONS = (
      'melo', 'mela', 'melos', 'melas',
      'telo', 'tela', 'telos', 'telas',
      'teme', 'tenos',
      'selo', 'sela', 'selos', 'selas',
      'sele', 'seles',
      'noslo', 'nosla', 'noslos', 'noslas',
      'oslo', 'osla', 'oslos', 'oslas',
      'osme', 'osnos'
  )

  INVALID_COMBINATIONS =  (
    {
      'error_type': u'le por se',
      'cases': [
        'lelo', 'lela', 'lelos',
        'lelas', 'leslo', 'lesla', 'leslos', 'leslas'
      ],
      'message':
        u"\tCuando 'le' o 'les' se juntan "
        u"con un complemento directo siempre "
        u"se cambian por 'se'."
    },
    {
      'error_type': u'orden OD OI incorrecto',
      'cases': [
        'lale', 'lole', 'lasle', 'losle',
        'loles', 'loles', 'lasles', 'losles',
        'lome', 'lote', 'lonos', 'loos',
        'mele', 'meles', 'tele', 'teles',
        'mese', 'nosse', 'tese', 'osse',
        'nosle', 'nosles', 'osle', 'osles'
      ],
      'message':
        u"\tSi por lo menos uno de los enclíticos es de tercera persona, "
        u"el orden correcto es Objeto Indirecto - Objeto Directo."
    },
    {
      'error_type': u'OI 3ra con OD 1ra o 2da',
      'cases': ['leme', 'lete', 'lenos', 'leos'],
      'message':
        u"\tSi los dos enclíticos son de tercera persona, "
        u"el orden correcto es Objeto Indirecto - Objeto Directo."
    },
    {
      'error_type': u'leísmo',
      'cases': [
        'lesle', 'leles', 'lese', 'lesse'
      #TODO special case for lese, lesse?
      ],
      'message':
        u"\tNo se pueden combinar dos pronombres indirectos."
    },     
    {
      'error_type': u'1ra persona delante de la 2da',
      'cases': ['mete', 'meos', 'noste', 'nosos'],
      'message':
        u'\tLa segunda persona tiene que '
        u'ir delante de la primera.'
    },
    {
      'error_type': u'Dos enclíticos de la misma persona',
      'cases': ['nosme', 'menos', 'oste', 'teos'],
      'message':
        u'\tNo se pueden combinar enclíticos '
        u'de la misma persona gramatical entre ellos, '
        u'salvo que sean de la tercera persona.'
    },
    {
      'error_type': u'Se repite el mismo pronombre',
      'cases':[
        'meme', 'tete', 'lala','lolo', 'sese',
        'nosnos','osos','laslas','loslos', 'lesles', 'lele'
      ],
      'message': u'\tNo se puede repetir el mismo pronombre.'
    }
  )

  #TODO acércasele!!!!!!!!!!!!!!

  VALID_MESSAGE = [ u"\n\tAquí tendremos un mensaje explicando "\
                    u"por qué esta combinación es válida y cómo "\
                    u"hay que combinar los enclíticos.",
                    u"\n\tMensaje explicando por qué esta combinación "\
                    u"es correcta y cómo combinar 3 enclíticos"
  ]                  

  INVALID_MESSAGE =[u"\n\tSin embargo, esta combinación no es válida.",
                    u"\n\tEsta combinación no es válida. "\
                    u"Mensaje sobre cómo combinar 3 enclíticos."
  ]                  
                        

  def __init__(self, combination):
    self.combination = ''.join(combination)
    length = len(combination)
    if length == 2:
      self.is_valid = self.combination in self.VALID_COMBINATIONS
    else:
      self.is_valid = False
      directs= ['la', 'lo', 'las', 'los']
      if combination[0] == 'se' and combination[1] != 'se':
        if combination[1] not in directs and combination[2] in directs:
          self.is_valid = 'True'
          
    self.error = None
    if self.is_valid:
      self.message = self.VALID_MESSAGE[length-2]
    else:
      self.message = self.INVALID_MESSAGE[length-2]
      if length == 2:
        for group in self.INVALID_COMBINATIONS:
          if self.combination in group['cases']:
            self.error = group['error_type']
            self.message += u'\t\n{}'.format(group['message'])
            break

























