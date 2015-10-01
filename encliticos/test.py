#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from encliticos.word import Word
from encliticos.structure import Structure
from encliticos.combination import Combination


class CombinationTests(unittest.TestCase):
  """
    Tests to check that the get_error() function of
    the Combination class returns the correct values.
  """

  def test_valid_combination(self):
    valid_combinations = [[u'se', u'la'], [u'me', u'los'],
                          [u'se', u'te', u'la']]
    for cb in valid_combinations:
      self.assertIsNone(Combination(cb).error)

    invalid_combinations = [[u'me', u'te'], [u'se', u'la', u'me'],
                            [u'la', u'te', u'los']]
    for cb in invalid_combinations:
       self.assertIsNotNone(Combination(cb).error)


class StructureTests(unittest.TestCase):
  """
  Tests to check whether the structure characteristics are
  defined correctly
  """

  def setUp(self):
    self.preguntaselo = Structure(
      True,
      [{
          "lema": "preguntar",
          "categoria": "VMIP3S0"
        },
        {
          "lema": "preguntar",
          "categoria": "VMM02S0"
        }
      ],
      ['se', 'lo']
    )
    self.damosnos = Structure(
      False,
      [{
        "lema": "dar",
        "categoria": "VMIP1P0"
        }
      ],
      ['nos']
    )
    self.tomandote = Structure(
      True,
      [{
      "lema": "tomar",
      "categoria": "VMG0000"
        }
      ],
      ['te']
    )
    self.pido = Structure(
      True,
      [{
      "lema": "pedir",
      "categoria": "VMIP1S0"
      }],
      []
    )
    self.tomarsemelos = Structure(
      True,
      [{
      "lema": "tomar",
      "categoria": "VMN0000"
        }
      ],
      ['se', 'me', 'los']
    )
    self.tomarselosme = Structure(
      True,
      [{
      "lema": "tomar",
      "categoria": "VMN0000"
        }
      ],
      ['se', 'los', 'me']
    )

  def test_has_combination(self):
    self.assertIsInstance(self.preguntaselo.combination, Combination)
    self.assertEqual(self.damosnos.combination, None)
    self.assertEqual(self.tomandote.combination, None)

  def test_is_asturianism(self):
    self.assertTrue(self.preguntaselo.valid)
    self.assertTrue(self.tomandote.valid)
    self.assertFalse(self.damosnos.valid)

  def test_can_be_reflexive(self):
    self.assertEqual(self.preguntaselo.reflexive, (False, False))
    self.assertEqual(self.tomandote.reflexive, (True, False))
    self.assertEqual(self.damosnos.reflexive, (True, True))
    self.assertEqual(self.tomarsemelos.reflexive, (True, True))


class WordTests(unittest.TestCase):
  """ Tests to check if the enclitics are identified correctly
      and if the word is correctly identidied as a verb
  """

  def setUp(self):
    self.los = Word(u'los')
    self.comer = Word(u'comer')
    self.dimelo = Word(u'dímelo')
    self.dimelo_wrong = Word(u'dimelo')
    self.tomaroslo = Word(u'tomároslo')
    self.tomaroslo_wrong = Word(u'tómaroslo')
    self.acentuamelo_wrong = Word(u'acentuamelo')
    self.darlole = Word(u'darlole')
    self.renidos = Word(u'reñidos')
    self.comeos = Word(u'comeos')
    self.vamonos = Word(u'vámonos')
    self.vamosnos = Word(u'vámosnos')
    self.demosela = Word(u'démosela')
    self.tomarosmela = Word(u'tomárosmela')
    self.tomarososla = Word(u'tomárososla')


  def test_bad_value(self):
    bad_values = [u'dime12', u'dime lo', u'']
    for value in bad_values:
      with self.assertRaises(ValueError):
        Word(value)

    with self.assertRaises(ValueError):
      Word(u'las').analyze_word()

  def test_syls_number(self):
    self.assertEqual(len(self.los.syllables), 1)
    self.assertEqual(len(self.tomaroslo.syllables), 4)

  def test_modify_ros_dos(self):
    self.assertEqual(self.tomaroslo.syllables[-2], u'os')
    self.assertEqual(self.renidos.syllables[-1], u'os')
    self.assertEqual(self.tomarosmela.syllables, 
                    [u'to',u'már', u'os', u'me', u'la'])
    self.assertEqual(self.tomarososla.syllables, 
                    [u'to', u'már', u'os', u'os', u'la'])

  def test_get_enclitics(self):
    self.assertEqual(self.demosela.get_enclitics(),
                        (u'démo', [u'se', u'la']))
    self.assertEqual(self.renidos.get_enclitics(),
                    (u'reñid', [u'os']))
    self.assertEqual(self.acentuamelo_wrong.get_enclitics(),
                        (u'acentua', [u'me', u'lo']))
    self.assertEqual(self.comer.get_enclitics(),
                        (u'comer', []))

  def test_irregular(self):
    pass
    # self.assertFalse(self.vamosnos.structures[0].is_regular)



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