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
                dfc22_parameters.UncertainCircle(
                    radius_proportion=dfc22_parameters.UncertainRange(0.2, 0.4),
                    activity_tuple_sequence=dfc22_parameters.UncertainSet(
                        [
                            [(0.25, False), (0.3, True), (0.8, False), (0.1, True)],
                            [(0.15, True), (0.8, False)],
                        ]
                    ),
                ),
                dfc22_parameters.UncertainTriangle(
                    rotation_angle=dfc22_parameters.UncertainRange(20, 30),
                    max_length=dfc22_parameters.UncertainRange(0.1, 0.5),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.9, 1.3),
                            dfc22_parameters.UncertainRange(0.7, 1.5),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ],
                    ),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                        ]
                    ),
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
                dfc22_parameters.UncertainTriangle(
                    rotation_angle=dfc22_parameters.UncertainRange(20, 30),
                    max_length=dfc22_parameters.UncertainRange(0.1, 0.5),
                    angle_proportion_sequence=dfc22_parameters.UncertainSequence(
                        [
                            dfc22_parameters.UncertainRange(0.9, 1.3),
                            dfc22_parameters.UncertainRange(0.7, 1.5),
                            dfc22_parameters.UncertainRange(0.8, 1),
                        ],
                    ),
                    is_side_active_sequence=dfc22_parameters.UncertainIsSideActiveSequence(
                        [
                            dfc22_parameters.UncertainSet([True, False]),
                            dfc22_parameters.UncertainSet([True, False]),
                            True,
                        ]
                    ),
                ),
            ],
        )
    )
    return alphabet


# alphabet0 = make_alphabet0()
#
# alphabet_to_noise_grid_video = dfc22_converters.AlphabetToNoiseGridVideo()
# alphabet_to_noise_grid_video.convert(alphabet0, "builds/video-noise-0.mp4")


# alphabet1 = make_alphabet1()
#
# alphabet_to_noise_grid_video = dfc22_converters.AlphabetToNoiseGridVideo(
#     letter_tuple_to_image=dfc22_converters.LetterTupleToImage(
#         background_color="white",
#         paper_canvas=dfc22_converters.PaperCanvas(1920, 1080),
#         x_whitespace=20,
#         y_whitespace=20,
#         letter_height=105,
#         x_margin=35,
#         y_margin=35,
#     ),
# )
# alphabet_to_noise_grid_video.convert(
#     alphabet1,
#     "builds/video-noise-1.mp4",
#     duration=25,
# )

# alphabet1 = make_alphabet1()
#
# alphabet_to_noise_grid_video = dfc22_converters.AlphabetToNoiseGridVideo(
#     letter_tuple_to_image=dfc22_converters.LetterTupleToImage(
#         background_color="white",
#         paper_canvas=dfc22_converters.PaperCanvas(1920, 1080),
#         x_whitespace=12,
#         y_whitespace=12,
#         letter_height=105,
#         x_margin=435,
#         y_margin=435,
#     ),
#     frame_size_tuple=(1, 4, 2, 4, 2, 1, 3, 2, 4, 2, 1, 3),
# )
# alphabet_to_noise_grid_video.convert(
#     alphabet1,
#     "builds/video-noise-2.mp4",
#     duration=15,
# )


alphabet2 = make_alphabet2()

alphabet_to_noise_grid_video = dfc22_converters.AlphabetToNoiseGridVideo(
    letter_tuple_to_image=dfc22_converters.LetterTupleToImage(
        background_color="white",
        paper_canvas=dfc22_converters.PaperCanvas(1920, 1080),
        x_whitespace=15,
        y_whitespace=15,
        letter_height=105,
        x_margin=335,
        y_margin=335,
    ),
    # frame_size_tuple=(1, 4, 2, 4, 2, 1, 3, 2, 4, 2, 1, 3),
)
alphabet_to_noise_grid_video.convert(
    alphabet2,
    "builds/video-noise-3.mp4",
    duration=15,
)
