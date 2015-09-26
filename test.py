#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from encliticos.word import Word
from encliticos.structure import Structure
from encliticos.combination import Combination


class CombinationTests(unittest.TestCase):
  """
    Test to check whether the validity of the enclitics
    combinations is determined correctly.
  """
  def setUp(self):
    self.sela = Combination(u'sela')
    self.melos = Combination(u'melos')
    self.lale = Combination(u'lale')
    self.mete = Combination(u'mete')

  def test_valid_combination(self):
    self.assertTrue(self.sela.is_valid)
    self.assertTrue(self.melos.is_valid)
    self.assertFalse(self.lale.is_valid)
    self.assertFalse(self.mete.is_valid)

  def test_error_type(self):
    self.assertEqual(self.lale.error, u'orden OD OI incorrecto')
    self.assertEqual(self.mete.error, u'1ra persona delante de la 2da')


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


class WordTests(unittest.TestCase):
  """ Tests to check if the enclitics are identified correctly
      and if the word is correctly identidied as a verb
  """

  def setUp(self):
    self.los = Word('los')
    self.comer = Word('comer')
    self.dimelo = Word('dímelo')
    self.dimelo_wrong = Word('dimelo')
    self.tomaroslo = Word('tomároslo')
    self.tomaroslo_wrong = Word('tómaroslo')
    self.acentuamelo_wrong = Word('acentuamelo')
    self.darlole = Word('darlole')
    self.renidos = Word('reñidos')
    self.comeos = Word('comeos')
    self.vamonos = Word('vámonos')
    self.vamosnos = Word('vámosnos')
    self.demosela = Word('démosela')

    # self.vamosnos.analyze_word()

  def test_bad_value(self):
    with self.assertRaises(ValueError):
      Word('dime12')
    with self.assertRaises(ValueError):
      Word('dime lo')
    with self.assertRaises(ValueError):
      Word('')  

  def test_syls_number(self):
    self.assertEqual(len(self.los.syllables), 1)
    self.assertEqual(len(self.tomaroslo.syllables), 4)

  def test_modify_ros_dos(self):
    self.assertEqual(self.tomaroslo.syllables[-2], 'os')
    self.assertEqual(self.renidos.syllables[-1], 'os')

  def test_get_enclitics(self):
    self.assertEqual(self.demosela.get_enclitics(),
                        ('démo', ['se', 'la']))
    self.assertEqual(self.renidos.get_enclitics(),
                    ('reñid', ['os']))
    self.assertEqual(self.acentuamelo_wrong.get_enclitics(),
                        ('acentua', ['me', 'lo']))
    self.assertEqual(self.comer.get_enclitics(),
                        ('comer', []))

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