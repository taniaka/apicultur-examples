

from apicultur.utils import ApiculturRateLimitSafe
try:
    from secret import ACCESS_TOKEN 
except ImportError:
    print(u"No encuentro el archivo 'secret.py' en este directorio con su ACCESS_TOKEN...")
    sys.exit(1)


pronouns =   {'la':'directo',
              'las': 'directo',
              'le': 'indirecto',
              'les': 'indirecto',
              'lo': 'directo',
              'los': 'directo',
              'nos': 'de tipo indefinido (directo o indirecto)',
              'me': 'de tipo indefinido (directo o indirecto)',
              'se': 'de tipo indefinido (directo o indirecto)',
              'os': 'de tipo indefinido (directo o indirecto)',
              'te': 'de tipo indefinido (directo o indirecto)'
            }


apicultur = ApiculturRateLimitSafe(ACCESS_TOKEN, "example")


def lematize(word):
  infinitives = []
  lemmas = apicultur.lematiza2(word=word)
  if lemmas:
    for lemma in lemmas['lemas']:
      category = lemma['categoria']
      if category[0] == 'V':
        infinitives.append(lemma['lema'])
    infinitives = list(set(infinitives))
  return infinitives    


def get_last(word, number):
  last_syllables = []
  syllabized = apicultur.silabeame(word=word)
  syllables = syllabized['palabraSilabeada'].split('=')
  for num in range(number):
    index = -(num+1)
    try:
      last_syllables.insert(0,syllables[index])
    except:
      break
  return last_syllables


def del_accent(word):
  new_word = word
  accents = {'á': 'a', 'ú':'u', 'í':'i', 'é':'e', 'ó':'o'}
  last_two = get_last(word, 2)
  if word[-1] == 'r':
    syllable = last_two[-1]
  else:
    syllable = last_two[0]
  for key, value in accents.items():
    if key in syllable:
      new_syllable = syllable.replace(key, value)
      new_word = word.replace(syllable, new_syllable)    
      break
  return new_word   


def detect_enclitics(word, last, second_last):
  enclitics = []
  length = 0
  verb = word

  if last in pronouns:
    if last != 'se':
      enclitics.append(last)
      length += len(last)
      if second_last in pronouns:
        enclitics.insert(0, second_last)
        length += len(second_last)  
    verb = word[0:-length]
    verb = del_accent(verb)

  return verb, enclitics  


def analyze_word(word):
  if word == '' or word == ' ':
    print('No has introducido nada, vuelve a intentar.')
    return

  print('Tu palabra es: {}.'.format(word.upper()))
  
  last_syllables = get_last(word, 2)
  last_syllables = ['os' if syllable == 'ros' else syllable for syllable in last_syllables]
  if len(last_syllables) < 2:
    print('Tu palabra solo tiene una sílaba '
          'y no puede tener enclíticos, intenta con otra palabra.')
    return

  last = last_syllables[-1]
  second_last = last_syllables[-2]
  verb, enclitics = detect_enclitics(word, last, second_last)

  lemas = lematize(verb)

  if not lemas:
    print('Parece que "{}" no es un verbo.'.
          format(word))

  else:

    if len(lemas) == 1:
      print('Tienes un verbo: {}.'.format(lemas[0]))
    else:
      print('Tienes un verbo que podría ser uno de los siguientes:')  
      for lema in lemas:
        print(lema)

    if not enclitics:
      print('No hemos detectado enclíticos.')

    elif len(enclitics) == 1:
      print('Tienes un enclítico de tipo complemento {}: {}.'.
            format(pronouns[last], last))

    elif len(enclitics) == 2:
      print("Tienes dos enclíticos")
      if second_last == "se":
        print("El primero es un complemento indirecto: {}, "
              "sustityendo al pronombre 'le' o 'les'.".
              format(second_last))
      else:
        print("El primero es un complemento indirecto: {}.".
              format(second_last))      
      print("El segundo es un complemento directo: {}.".
            format(last))

analyze_word("dime")
analyze_word("preguntaros")
analyze_word("dárosla")
analyze_word("tomárselas")
analyze_word("pónselas")
analyze_word("pregúntatela")
analyze_word("sálvanos")
analyze_word("acercaros")
analyze_word(' ')
analyze_word("trabajo")
analyze_word("burros")
analyze_word("majos")
analyze_word("mala")
analyze_word("las")
analyze_word("verde")


