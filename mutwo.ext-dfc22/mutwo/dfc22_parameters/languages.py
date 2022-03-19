from __future__ import annotations
import dataclasses
import typing

from mutwo import zimmermann_generators

__all__ = ("NonTerminalPair",)


@dataclasses.dataclass(frozen=True)
class NonTerminalPair(object):
    consonant: zimmermann_generators.JustIntonationPitchNonTerminal = zimmermann_generators.JustIntonationPitchNonTerminal()
    vowel: zimmermann_generators.JustIntonationPitchNonTerminal = zimmermann_generators.JustIntonationPitchNonTerminal()

    def __hash__(self) -> int:
        return hash(
            self.consonant.exponent_tuple + ("SEPARATOR",) + self.vowel.exponent_tuple
        )

    def _calculate(
        self,
        other: NonTerminalPair,
        operation: typing.Callable[
            [
                zimmermann_generators.JustIntonationPitchNonTerminal,
                zimmermann_generators.JustIntonationPitchNonTerminal,
            ],
            zimmermann_generators.JustIntonationPitchNonTerminal,
        ],
    ) -> NonTerminalPair:
        return type(self)(
            consonant=operation(self.consonant, other.consonant),
            vowel=operation(self.vowel, other.vowel),
        )

    def __add__(self, other: NonTerminalPair) -> NonTerminalPair:
        return self._calculate(
            other,
            lambda pitch0, pitch1: zimmermann_generators.JustIntonationPitchNonTerminal(
                pitch0 + pitch1
            ),
        )

    def __sub__(self, other: NonTerminalPair) -> NonTerminalPair:
        return self._calculate(
            other,
            lambda pitch0, pitch1: zimmermann_generators.JustIntonationPitchNonTerminal(
                pitch0 - pitch1
            ),
        )

    def __eq__(self, other: typing.Any) -> bool:
        try:
            return self.consonant == other.consonant and self.vowel == other.vowel
        except AttributeError:
            return False
