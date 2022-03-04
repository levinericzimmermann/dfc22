from mutwo import music_events


__all__ = ("NoteLikeWithPhoneme", "NoteLikeWithVowelAndConsonantTuple")


class NoteLikeWithPhoneme(music_events.NoteLike):
    def __init__(self, *args, phoneme: str = "a", **kwargs):
        self.phoneme = phoneme
        super().__init__(*args, **kwargs)


class NoteLikeWithVowelAndConsonantTuple(music_events.NoteLike):
    def __init__(
        self,
        *args,
        vowel: str = "a",
        consonant_tuple: tuple[str, ...] = tuple([]),
        **kwargs
    ):
        self.vowel = vowel
        self.consonant_tuple = consonant_tuple
        super().__init__(*args, **kwargs)
