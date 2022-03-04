import copy

from mutwo import core_events
from mutwo import csound_converters
from mutwo import dfc22_converters
from mutwo import dfc22_events
from mutwo import dfc22_generators
from mutwo import isis_converters
from mutwo import mbrola_converters
from mutwo import music_parameters
from mutwo import zimmermann_generators


def render_mbrola(
    sentence_to_render: core_events.SequentialEvent[dfc22_events.Word],
    path: str = "builds/sentence-mbrola.wav",
    initial_pitch=music_parameters.JustIntonationPitch("1/2"),
    initial_pulse=music_parameters.JustIntonationPitch("1/4"),
):
    sentence_to_mbrola_sequential_event = dfc22_converters.SentenceToSequentialEvent()
    sequential_event_to_mbrola_sound_file = mbrola_converters.EventToSpeakSynthesis()
    sequential_event_mbrola, *_ = sentence_to_mbrola_sequential_event.convert(
        sentence_to_render,
        initial_pitch=initial_pitch,
        initial_pulse=initial_pulse,
    )
    sequential_event_to_mbrola_sound_file.convert(sequential_event_mbrola, path)


def render_isis(
    sentence_to_render: core_events.SequentialEvent[dfc22_events.Word],
    path: str = "builds/sentence-mbrola.wav",
    initial_pitch=music_parameters.JustIntonationPitch("1/2"),
    initial_pulse=music_parameters.JustIntonationPitch("1/4"),
):
    sentence_to_isis_sequential_event = dfc22_converters.SentenceToSequentialEvent(
        dfc22_converters.WordToSequentialEvent(
            dfc22_events.NoteLikeWithVowelAndConsonantTuple
        )
    )
    sequential_event_to_isis_sound_file = isis_converters.IsisConverter(
        isis_converters.IsisScoreConverter(),
        "--cfg_synth etc/isis-cfg-synth.cfg",
        "--cfg_style etc/isis-cfg-style.cfg",
        "--seed 100",
    )

    [dfc22_converters.prepare_word_for_isis(word) for word in sentence_to_render]
    sequential_event_isis, *_ = sentence_to_isis_sequential_event.convert(
        sentence_to_render,
        initial_pitch=initial_pitch,
        initial_pulse=initial_pulse,
    )

    def is_rest(note_like):
        return note_like.vowel == "_"

    def process_surviving_event(event0, event1):
        event0.duration += event1.duration
        event0.pitch_list = [music_parameters.MidiPitch(0)]

    sequential_event_isis.tie_by(
        lambda event0, event1: is_rest(event0) and is_rest(event1),
        process_surviving_event,
    )
    sequential_event_to_isis_sound_file.convert(sequential_event_isis, path)


def render_sine(
    sentence_to_render: core_events.SequentialEvent[dfc22_events.Word],
    path: str = "builds/sentence-mbrola.wav",
    initial_pitch=music_parameters.JustIntonationPitch("1/2"),
    initial_pulse=music_parameters.JustIntonationPitch("1/4"),
):
    sentence_to_sequential_event = dfc22_converters.SentenceToSequentialEvent(
        dfc22_converters.WordToSequentialEvent(
            dfc22_events.NoteLikeWithVowelAndConsonantTuple
        )
    )
    sequential_event_to_sine_sound_file = csound_converters.EventToSoundFile(
        "etc/sine.orc",
        csound_converters.EventToCsoundScore(
            p4=lambda note_like: note_like.pitch_list[0].frequency
            if note_like.pitch_list
            else None
        ),
    )

    sequential_event, *_ = sentence_to_sequential_event.convert(
        sentence_to_render,
        initial_pitch=initial_pitch,
        initial_pulse=initial_pulse,
    )

    sequential_event_to_sine_sound_file.convert(sequential_event, path)


def render_noise(
    sentence_to_render: core_events.SequentialEvent[dfc22_events.Word],
    path: str = "builds/sentence-mbrola.wav",
    initial_pitch=music_parameters.JustIntonationPitch("1/2"),
    initial_pulse=music_parameters.JustIntonationPitch("1/4"),
):
    sentence_to_sequential_event = dfc22_converters.SentenceToSequentialEvent(
        dfc22_converters.WordToSequentialEvent(
            dfc22_events.NoteLikeWithVowelAndConsonantTuple
        )
    )
    sequential_event_to_sound_file = csound_converters.EventToSoundFile(
        "etc/noise.orc",
        csound_converters.EventToCsoundScore(
            p4=lambda note_like: 0.5 if note_like.consonant_tuple else 0
        ),
    )

    sequential_event, *_ = sentence_to_sequential_event.convert(
        sentence_to_render,
        initial_pitch=initial_pitch,
        initial_pulse=initial_pulse,
    )
    sequential_event_to_sound_file.convert(sequential_event, path)


sentence_generator_tuple = (
    dfc22_generators.SentenceGenerator(
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            3,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            3,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            3,
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            2,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            3,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            4,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("8/7"),
            3,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/7"),
            2,
        ),
    ),
    dfc22_generators.SentenceGenerator(
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            4,
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            5,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("8/7"),
            4,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/7"),
            5,
        ),
    ),
    dfc22_generators.SentenceGenerator(
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            3,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            1,
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            1,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            2,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            2,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/9"),
            2,
        ),
    ),
)
pitch_tuple = (
    music_parameters.JustIntonationPitch("2/1"),
    music_parameters.JustIntonationPitch("1/1"),
    music_parameters.JustIntonationPitch("1/2"),
    music_parameters.JustIntonationPitch("1/3"),
    music_parameters.JustIntonationPitch("1/4"),
)
pulse_tuple = (
    music_parameters.JustIntonationPitch("1/2"),
    music_parameters.JustIntonationPitch("1/3"),
    music_parameters.JustIntonationPitch("1/4"),
    music_parameters.JustIntonationPitch("1/5"),
)
# render_engine_tuple = (("isis", render_isis), ("mbrola", render_mbrola))
# render_engine_tuple = (("sine", render_sine),)
render_engine_tuple = (("noise-s", render_noise),)
n_sentences_per_generator = 4

base_path = "builds/sentences"
for nth_sentence_generator, sentence_generator in enumerate(sentence_generator_tuple):
    for nth_sentence in range(n_sentences_per_generator):
        sentence = next(sentence_generator)
        for initial_pitch in pitch_tuple:
            for initial_pulse in pulse_tuple:
                for engine_name, render_engine in render_engine_tuple:
                    path = (
                        f"{base_path}/{nth_sentence_generator}/{nth_sentence}_{engine_name}_"
                        f"{str(initial_pitch.ratio).replace('/', '-')}_"
                        f"{str(initial_pulse.ratio).replace('/', '-')}.wav"
                    )
                    render_engine(
                        copy.deepcopy(sentence), path, initial_pitch, initial_pulse
                    )
