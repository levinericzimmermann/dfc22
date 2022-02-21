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

from mutwo import dfc22_parameters


__all__ = ("Alphabet",)

class Alphabet(tuple[dfc22_parameters.Letter, ...]):
    pass
