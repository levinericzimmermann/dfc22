from mutwo import dfc22_converters
from mutwo import dfc22_parameters

import dfc22


def make_alphabet0():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
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
    return alphabet


def make_alphabet1():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
    alphabet = phoneme_tree.create_alphabet(
        dfc22_parameters.UncertainLetter(
            letter_canvas=dfc22_parameters.LetterCanvas(400, 800),
            uncertain_letter_element_sequence=[
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
    return alphabet


def make_alphabet2():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
    alphabet = phoneme_tree.create_alphabet(
        dfc22_parameters.UncertainLetter(
            letter_canvas=dfc22_parameters.LetterCanvas(400, 800),
            uncertain_letter_element_sequence=[
                dfc22_parameters.UncertainQuad(
                    length_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 1.5),
                            dfc22_parameters.UncertainRange(0.5, 1),
                        ]
                    ),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.2, 0.94),
                            dfc22_parameters.UncertainRange(1, 2),
                            dfc22_parameters.UncertainRange(0.2, 1),
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
    return alphabet


def make_alphabet3():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
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
    return alphabet


def make_alphabet4():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
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
                dfc22_parameters.UncertainHexagon(
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(1, 1.5),
                            dfc22_parameters.UncertainRange(0.8, 1),
                            dfc22_parameters.UncertainRange(1, 1,3),
                            dfc22_parameters.UncertainRange(0.7, 1),
                            dfc22_parameters.UncertainRange(1, 1.3),
                            dfc22_parameters.UncertainRange(0.9, 1),
                        ]
                    ),
                    length_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.8, 1),
                            dfc22_parameters.UncertainRange(0.6, 1.2),
                            dfc22_parameters.UncertainRange(0.5, 1.2),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(0.3, 0.4),
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
                dfc22_parameters.UncertainPentagon(
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.9, 1.3),
                            dfc22_parameters.UncertainRange(0.8, 1.3),
                            dfc22_parameters.UncertainRange(0.8, 1),
                            dfc22_parameters.UncertainRange(0.7, 1.2),
                            dfc22_parameters.UncertainRange(0.4, 1),
                        ]
                    ),
                    max_length=dfc22_parameters.UncertainRange(0.3, 1),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            dfc22_parameters.UncertainSet([True, False]),
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
    return alphabet


def make_alphabet5():
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

    node_to_specify_letter_dict = {dfc22.trees.ROOT_NODE_NAME: phoneme_root_converter}
    for phoneme_group_name in dfc22.trees.PHONEME_GROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_group_name: phoneme_group_converter}
        )
    for phoneme_subgroup_name in dfc22.trees.PHONEME_SUBGROUP_TUPLE:
        node_to_specify_letter_dict.update(
            {phoneme_subgroup_name: phoneme_subgroup_converter}
        )

    phoneme_tree = dfc22.trees.PhonemeTree(
        node_to_specify_letter=node_to_specify_letter_dict
    )
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
                    max_length=dfc22_parameters.UncertainRange(0.1, 0.3),
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
                    max_length=dfc22_parameters.UncertainRange(0.5, 1),
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
    return alphabet


ALPHABET0 = make_alphabet0()
ALPHABET1 = make_alphabet1()
ALPHABET2 = make_alphabet2()
ALPHABET3 = make_alphabet3()
ALPHABET4 = make_alphabet4()
ALPHABET5 = make_alphabet5()

alphabet_tuple = (ALPHABET0, ALPHABET1, ALPHABET2, ALPHABET3, ALPHABET4, ALPHABET5)

path_list = []
for sequential_event_index, sequential_event, alphabet in zip(
    range(6), dfc22.constants.SIMULTANEOUS_EVENT_WITH_NOTES, alphabet_tuple
):
    path = f"builds/video_{sequential_event_index}.mp4"
    sequential_event_to_video = dfc22_converters.SequentialEventToVideo(alphabet)

    sequential_event_to_video.convert(sequential_event[:40], path)
    path_list.append(path)


size = (1920, 1080)
# for grid_index, grid in enumerate([(3, 2), (6, 1)]):
# for grid_index, grid in enumerate([(4, 2), (6, 1)]):
for grid_index, grid in enumerate([(4, 2),]):
    video_path_sequence_to_video_grid = dfc22_converters.VideoPathSequenceToVideo(
        grid=grid, size=size
    )
    video_path_sequence_to_video_grid.convert(
        path_list, f"builds/video_grid_{grid_index}.mp4"
    )
