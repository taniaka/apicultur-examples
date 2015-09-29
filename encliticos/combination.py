#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Combination:

  # VALID_COMBINATIONS = (
  #     'melo', 'mela', 'melos', 'melas',
  #     'telo', 'tela', 'telos', 'telas',
  #     'teme', 'tenos',
  #     'selo', 'sela', 'selos', 'selas',
  #     'sele', 'seles',
  #     'noslo', 'nosla', 'noslos', 'noslas',
  #     'oslo', 'osla', 'oslos', 'oslas',
  #     'osme', 'osnos'
  # )

  INVALID_COMBINATIONS =  {
    'two_encls':(
      {
        'cases': [
          'lelo', 'lela', 'lelos',
          'lelas', 'leslo', 'lesla', 'leslos', 'leslas'
        ],
        'error': u'le por se',
        'message':
          u"\tCuando 'le' o 'les' se juntan "
          u"con un complemento directo siempre "
          u"se cambian por 'se'."
      },

      {
        'cases': [
          'lale', 'lole', 'lasle', 'losle',
          'loles', 'loles', 'lasles', 'losles',
          'losle', 'lose', 'losse', 'lasse',
          'lame', 'late', 'lanos', 'laos',
          'lasme', 'laste', 'lasnos', 'lasos',
          'lome', 'lote', 'lonos', 'loos',
          'mele', 'meles', 'tele', 'teles',
          'mese', 'nosse', 'tese', 'osse',
          'nosle', 'nosles', 'osle', 'osles'
        ],
        'error': u'orden OD OI incorrecto',
        'message':
          u"\tSi por lo menos uno de los enclíticos es de tercera persona, "
          u"el orden correcto es Objeto Indirecto - Objeto Directo."
      },
      {
        'cases': ['leme', 'lete', 'lenos', 'leos'],
        'error': u'OI 3ra con OD 1ra o 2da',
        'message':
          u"\tSi los dos enclíticos son de tercera persona, "
          u"el orden correcto es Objeto Indirecto - Objeto Directo."
      },
      {
        'cases': [
          'lesle', 'leles', 'lese', 'lesse'
        #TODO special case for lese, lesse?
        ],
        'error': u'leísmo',
        'message':
          u"\tNo se pueden combinar dos pronombres indirectos."
      },     
      {
        'cases': ['mete', 'meos', 'noste', 'nosos'],
        'error': u'1ra persona delante de la 2da',
        'message':
          u'\tLa segunda persona tiene que '
          u'ir delante de la primera.'
      },
      {
        'cases': ['nosme', 'menos', 'oste', 'teos'],
        'error': u'Dos enclíticos de la misma persona',
        'message':
          u'\tNo se pueden combinar enclíticos '
          u'de la misma persona gramatical entre ellos, '
          u'salvo que sean de la tercera persona.'
      },
      {
        'cases':[
          'meme', 'tete', 'lala','lolo', 'sese',
          'nosnos','osos','laslas','loslos', 'lesles', 'lele'
        ],
        'error': u'Se repite el mismo pronombre',
        'message': u'\tNo se puede repetir el mismo pronombre.'
      }
    ),

    'three_encls': {
        'error': 'Error de combinación de 3 enclíticos.',
        'message': 'Explicar los errores específicos para 3 enclíticos.'
    }
    
  }
  #TODO acércasele!!!!!!!!!!!!!!

  # VALIDITY_MESSAGE = {
  #   True: [ u"\n\tAquí tendremos un mensaje explicando "\
  #           u"por qué esta combinación es válida y cómo "\
  #           u"hay que combinar dos enclíticos.",
  #           u"\n\tMensaje explicando por qué esta combinación "\
  #           u"es correcta y cómo combinar 3 enclíticos"
  #   ],
  #   False: [u"\n\tSin embargo, esta combinación no es válida.",
  #           u"\n\tEsta combinación no es válida. "\
  #           u"Mensaje sobre cómo combinar 3 enclíticos."
  #   ]
  # }

  VALID_MESSAGE = [ u"\n\tAquí tendremos un mensaje explicando "\
                    u"por qué esta combinación es válida y cómo "\
                    u"hay que combinar dos enclíticos.",
                    u"\n\tMensaje explicando por qué esta combinación "\
                    u"es correcta y cómo combinar 3 enclíticos"
  ]                  

  INVALID_MESSAGE =[u"\n\tSin embargo, esta combinación no es válida.\n\t",
                    u"\n\tEsta combinación no es válida. "\
                    u"\n\tMensaje sobre cómo combinar 3 enclíticos.\n\t"
  ]                  
                        

  def __init__(self, combination):    
    self.combination = combination
    self.error, self.message = self.get_error()

  def get_error(self):
    last_two = ''.join(self.combination[-2:])
    length = len(self.combination)
    error = None
    message = self.VALID_MESSAGE[length-2]

    for group in self.INVALID_COMBINATIONS['two_encls']:
      if last_two in group['cases']:
        error = group['error']
        message = self.INVALID_MESSAGE[length-2] + group['message']

    if length == 3:
      first = self.combination[0]
      if first not in ['se', 'me', 'te', 'nos', 'os'] or first in last_two:
        three_invalid = self.INVALID_COMBINATIONS['three_encls']
        if not error:
          error = three_invalid['error']
          message = self.INVALID_MESSAGE[1]
        message += three_invalid['message']

    return error, message

























