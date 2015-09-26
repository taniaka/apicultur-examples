#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from .word import Word


class TestEncliticos(unittest.TestCase):
  """
  Aquí aparecen casos de uso de enclíticos para comprobar que el
  código se está comportando como debe.
  """
  # TODO (lingüistas): Añadir los tests que se consideren adecuados

  def test_encliticos(self):
      data = Word("diselo").analyze_word()
      self.assertEqual(data, '<lo que tenga que devolver>')

  def test_leismos(self):
      pass

  def test_laismos(self):
      pass

  def test_loismos(self):
      pass




class TestConnection(unittest.TestCase):
  """
  En esta clase se definen una serie de tests para confirmar que las
  APIs de Apicultur están disponibles, que el ACCESS_TOKEN introducido
  tiene acceso a ellas y que algunas llamadas de ejemplo devuelven
  valores válidos.
  """

  @classmethod
  def setUp(cls):
    from apicultur.utils import ApiculturRateLimitSafe
    from secret import ACCESS_TOKEN
    cls.api = ApiculturRateLimitSafe(ACCESS_TOKEN)

  def test_silabeame(self):
    data = self.api.silabeame(word=u"perro")
    self.assertEqual(data[u'palabraSilabeada'], u'pe=rro')
    self.assertEqual(data[u'silabaTonica'], u'pe')
    self.assertEqual(data[u'numeroSilabas'], 2)
    self.assertEqual(data[u'posSilabaTonica'], 2)

  def test_lematiza2(self):
    data = self.api.lematiza2(word=u"meses")
    self.assertEqual(data[u'palabra'], u'meses')
    lemas = data[u'lemas']
    self.assertEqual(len(lemas), 2)



if __name__ == '__main__':
    unittest.main()