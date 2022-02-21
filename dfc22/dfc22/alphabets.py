"""Create made-up alphabets based on phonetic relations.

The basic structure is:

  Set[Elements]

    This is an unspecified letter.
    In the end we will take all remaining elements
    of this set and combine them to create our letter.

  Element

    This is one unspecified LetterElement (a circle, a
    polygon or an ellipsis).


The evolution is:

  Urletter ->

      LetterVocal     ->

          LetterOpen        ->
          ...               ->

      LetterConsonant ->

          LetterPulsive     ->
          ...               ->


To split our Urletter (and each UnspecifiedLetter of
the next generations) we use the class `SpecifyLetter`.
Each node has a specific instance of the class.
If a node has no specification for the class it will
simply use the same instance as the parent node.

  SpecifyLetter

    Split the set of all available elements to the next
    generation of letters. It will also adjust or specify
    the elements.
"""

from mutwo import dfc22_converters
from mutwo import dfc22_generators


def specify_letter():
    uncertain_letter = dfc22_generators.UncertainLetter()
    specify_uncertain_letter = dfc22_converters.SpecifyUncertainLetter()
    specified_letter_list = specify_uncertain_letter.convert(uncertain_letter, 5)
    letter_list = [sl.resolve() for sl in specified_letter_list]
    for nth, letter in enumerate(letter_list):
        print(letter)
        letter.image.save(f'img-test-{nth}.png')
