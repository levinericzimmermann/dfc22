import typing

import treelib

from mutwo import dfc22_converters
from mutwo import dfc22_parameters
from mutwo import isis_converters


ROOT_NODE_NAME = "phoneme"
PHONEME_GROUP_TUPLE = ("vowel", "consonant")
PHONEME_SUBGROUP_TUPLE = (
    "a-vowel",
    "e-vowel",
    "o-vowel",
    "i-vowel",
    "u-vowel",
    "voiced_fricative",
    "unvoiced_fricative",
    "voiced_plosive",
    "nasal",
    "other",
)


class PhonemeTree(treelib.Tree):
    structure = {
        "vowel": {
            "a-vowel": ("a", "@", "a~"),
            "e-vowel": ("e", "E", "e~"),
            "o-vowel": ("o", "O", "o~", "2", "9", "9~"),
            "i-vowel": ("i",),
            "u-vowel": ("u", "y"),
        },
        "consonant": {
            "semi_vowel_tuple": isis_converters.constants.XSAMPA.semi_vowel_tuple,
            "voiced_fricative": isis_converters.constants.XSAMPA.voiced_fricative_tuple,
            "unvoiced_fricative": isis_converters.constants.XSAMPA.unvoiced_fricative_tuple,
            "voiced_plosive": isis_converters.constants.XSAMPA.voiced_plosive_tuple,
            "unvoiced_plosive": isis_converters.constants.XSAMPA.unvoiced_plosive_tuple,
            "nasal": isis_converters.constants.XSAMPA.nasal_tuple,
            "other": isis_converters.constants.XSAMPA.other_tuple,
        },
    }
    node_id_suffix = "node"

    NodeToSpecifyLetter = dict[str, dfc22_converters.SpecifyUncertainLetter]

    def __init__(
        self,
        *args,
        node_to_specify_letter: NodeToSpecifyLetter = {
            ROOT_NODE_NAME: dfc22_converters.SpecifyUncertainLetter()
        },
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._add_node(ROOT_NODE_NAME, None, node_to_specify_letter)
        for phoneme_group_name, phoneme_group in self.structure.items():
            self._add_node(phoneme_group_name, ROOT_NODE_NAME, node_to_specify_letter)
            for phoneme_subgroup_name, phoneme_subgroup in phoneme_group.items():
                self._add_node(
                    phoneme_subgroup_name, phoneme_group_name, node_to_specify_letter
                )
                for phoneme in phoneme_subgroup:
                    self._add_node(
                        phoneme, phoneme_subgroup_name, node_to_specify_letter
                    )

    def _add_node(
        self,
        name: str,
        parent: typing.Optional[str],
        node_to_specify_letter: NodeToSpecifyLetter,
    ):
        try:
            data = node_to_specify_letter[name]
        except KeyError:
            data = None
        self.create_node(name, name, parent=parent, data=data)

    def phoneme_to_node_id(self, phoneme: str) -> str:
        return f"{phoneme}_{self.node_id_suffix}"

    def _get_specify_letter(
        self, node: treelib.Node
    ) -> dfc22_converters.SpecifyUncertainLetter:
        if node.data:
            return node.data
        else:
            return self._get_specify_letter(self[node.bpointer])

    def create_alphabet(
        self,
        urletter: dfc22_parameters.UncertainLetter = dfc22_parameters.UncertainLetter(),
    ) -> dfc22_parameters.Alphabet:
        def get_letter_list(
            uncertain_letter: dfc22_parameters.UncertainLetter, node: treelib.Node
        ) -> list[dfc22_parameters.Letter]:
            child_id_list = node.fpointer
            if child_id_list:
                child_node_list = [self[child_id] for child_id in child_id_list]
                uncertain_letter_tuple = self._get_specify_letter(node)(
                    uncertain_letter, len(child_node_list)
                )
                letter_list = []
                for child_node, child_uncertain_letter in zip(
                    child_node_list, uncertain_letter_tuple
                ):
                    letter_list.extend(
                        get_letter_list(child_uncertain_letter, child_node)
                    )
            else:
                letter_list = [
                    uncertain_letter.resolve(
                        phoneme_list=[[dfc22_parameters.XSAMPAPhoneme(node.tag)]]
                    )
                ]
            return letter_list

        node = self[self.root]
        return dfc22_parameters.Alphabet(
            get_letter_list(urletter, node)
            + [
                dfc22_parameters.Letter(
                    urletter.argument_to_resolvable_object_dict["letter_canvas"],
                    [],
                    [[dfc22_parameters.XSAMPAPhoneme("_")]],
                )
            ]
        )


def main():
    phoneme_root_converter = dfc22_converters.SpecifyUncertainLetter(
        0.6,
        specify_uncertain_letter_element=dfc22_converters.SpecifyUncertainLetterElement(
            {
                dfc22_parameters.UncertainRange: dfc22_converters.SymmetricalSpecifyUncertainRange(
                    2
                ),
                dfc22_parameters.UncertainSet: dfc22_converters.SpecifyUncertainSet(),
                dfc22_parameters.UncertainDict: dfc22_converters.SpecifyUncertainDict(),
                dfc22_parameters.UncertainIsSideActiveSequence: dfc22_converters.SpecifyUncertainIsSideActiveSequence(),
            }
        ),
    )
    phoneme_group_converter = dfc22_converters.SpecifyUncertainLetter(
        0.75,
        specify_uncertain_letter_element=dfc22_converters.SpecifyUncertainLetterElement(
            {
                dfc22_parameters.UncertainRange: dfc22_converters.SymmetricalSpecifyUncertainRange(
                    0.5
                ),
                dfc22_parameters.UncertainSet: dfc22_converters.SpecifyUncertainSet(),
                dfc22_parameters.UncertainDict: dfc22_converters.SpecifyUncertainDict(),
                dfc22_parameters.UncertainIsSideActiveSequence: dfc22_converters.SpecifyUncertainIsSideActiveSequence(),
            }
        ),
    )
    phoneme_subgroup_converter = dfc22_converters.SpecifyUncertainLetter(
        0.95,
        specify_uncertain_letter_element=dfc22_converters.SpecifyUncertainLetterElement(
            {
                dfc22_parameters.UncertainRange: dfc22_converters.SymmetricalSpecifyUncertainRange(
                    0.25
                ),
                dfc22_parameters.UncertainSet: dfc22_converters.SpecifyUncertainSet(),
                dfc22_parameters.UncertainDict: dfc22_converters.SpecifyUncertainDict(),
                dfc22_parameters.UncertainIsSideActiveSequence: dfc22_converters.SpecifyUncertainIsSideActiveSequence(),
            }
        ),
    )

    node_to_specify_letter_dict = {ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = PhonemeTree(node_to_specify_letter=node_to_specify_letter_dict)
    alphabet = phoneme_tree.create_alphabet(
        dfc22_parameters.UncertainLetter(
            letter_canvas=dfc22_parameters.LetterCanvas(400, 800),
            uncertain_letter_element_sequence=[
                dfc22_parameters.UncertainQuad(
                    length_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 1.2),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ]
                    ),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.5, 0.94),
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.6, 1),
                            dfc22_parameters.UncertainRange(1.2, 2),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(0.5, 0.9),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            True,
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                        ]
                    ),
                ),
                dfc22_parameters.UncertainHexagon(
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(2, 3),
                            dfc22_parameters.UncertainRange(0.1, 0.3),
                            dfc22_parameters.UncertainRange(2, 3),
                            dfc22_parameters.UncertainRange(0.5, 1),
                            dfc22_parameters.UncertainRange(2, 3),
                            dfc22_parameters.UncertainRange(2, 3),
                        ]
                    ),
                    length_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 1.2),
                            dfc22_parameters.UncertainRange(0.8, 1),
                            dfc22_parameters.UncertainRange(1, 1.2),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(0.7, 0.9),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                        ]
                    ),
                ),
                dfc22_parameters.UncertainHexagon(
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.5, 0.8),
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.5, 1),
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.5, 1),
                        ]
                    ),
                    length_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.8, 1),
                            dfc22_parameters.UncertainRange(1, 1.2),
                            dfc22_parameters.UncertainRange(1, 1.2),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(0.5, 0.9),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                        ]
                    ),
                ),
                dfc22_parameters.UncertainTriangle(
                    rotation_angle=dfc22_parameters.UncertainRange(0, 30),
                    max_length=dfc22_parameters.UncertainRange(0.6, 1.2),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.5, 0.6),
                            dfc22_parameters.UncertainRange(1, 2.2),
                        ]
                    ),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            False,
                        ]
                    ),
                ),
                dfc22_parameters.UncertainTriangle(
                    rotation_angle=dfc22_parameters.UncertainRange(0, 30),
                    max_length=dfc22_parameters.UncertainRange(0.7, 1),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.9, 1.3),
                            dfc22_parameters.UncertainRange(0.7, 1.5),
                            dfc22_parameters.UncertainRange(0.1, 1),
                        ],
                    ),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            False,
                        ]
                    ),
                ),
                dfc22_parameters.UncertainCircle(
                    radius_proportion=dfc22_parameters.UncertainRange(0.4, 0.7),
                    activity_tuple_sequence=dfc22_parameters.UncertainSet(
                        [
                            [(0.25, False), (0.3, True), (0.8, False), (0.1, True)],
                            [(0.15, True), (0.8, False)],
                        ]
                    ),
                ),
                dfc22_parameters.UncertainCircle(
                    radius_proportion=dfc22_parameters.UncertainRange(0.7, 0.95),
                    activity_tuple_sequence=dfc22_parameters.UncertainSet(
                        [
                            [(0.9, True), (0.3, False)],
                            [(0.15, True), (0.8, False)],
                        ]
                    ),
                ),
                dfc22_parameters.UncertainCircle(
                    radius_proportion=dfc22_parameters.UncertainRange(0.1, 0.2),
                    activity_tuple_sequence=dfc22_parameters.UncertainSet(
                        [
                            [(0.25, False), (0.3, True), (0.8, False), (0.1, True)],
                            [(0.25, True), (0.8, False)],
                        ]
                    ),
                ),
                dfc22_parameters.UncertainPentagon(
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.9, 1.3),
                            dfc22_parameters.UncertainRange(0.7, 1.5),
                            dfc22_parameters.UncertainRange(0.1, 1),
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.1, 1),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(2, 3),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                            dfc22_parameters.UncertainSet([True, False]),
                        ]
                    ),
                    rotation_angle=dfc22_parameters.UncertainRange(0, 20),
                ),
            ],
        )
    )

    from mutwo import dfc22_generators
    from mutwo import zimmermann_generators

    sentence_generator = dfc22_generators.SentenceGenerator(
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("9/7"),
            3,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            5,
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            4,
        ),
        dfc22_generators.make_word_tuple(
            zimmermann_generators.JustIntonationPitchNonTerminal("7/8"),
            1,
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
            2,
            zimmermann_generators.JustIntonationPitchNonTerminal("8/7"),
            1,
        ),
    )

    sentence0 = next(sentence_generator)
    for _ in range(10):
        sentence0 += next(sentence_generator)

    sentence_to_letter_tuple = dfc22_converters.SentenceToLetterTuple(
        dfc22_converters.WordToLetterTuple(alphabet)
    )
    letter_tuple_to_image = dfc22_converters.LetterTupleToImage()
    letter_tuple = sentence_to_letter_tuple(sentence0)
    letter_tuple_to_image.convert(letter_tuple, "builds/letter.png")

    for letter in alphabet:
        letter.image.save(f"builds/alphabets/{letter.phoneme_list[0][0]}.png")

    from PIL import Image

    image_to_encoded_image = dfc22_converters.ImageToEncodedImage(
        alphabet,
        contrast_factor=3,
        inverse=False,
        resize_image_width=60,
        pixel_resize_factor_tuple=(30, 60),
    )
    image_to_convert = Image.open("mutwo.ext-dfc22/tests/converters/queen.jpg")
    converted_image = image_to_encoded_image.convert(image_to_convert)
    converted_image_path = "queen_converted.jpg"
    converted_image.save(converted_image_path)


if __name__ == "__main__":
    main()
