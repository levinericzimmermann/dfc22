from mutwo import dfc22_parameters

DEFAULT_UNCERTAIN_DURATION_FOR_PHONEME_GROUP = dfc22_parameters.UncertainRange(0.3, 0.6)

DEFAULT_UNCERTAIN_REST_DURATION_FOR_PHONEME_GROUP = dfc22_parameters.UncertainRange(
    0.1, 0.2
)

DEFAULT_UNCERTAIN_REST_DURATION_FOR_WORD = dfc22_parameters.UncertainRange(0.4, 1.2)

DEFAULT_UNCERTAIN_REST_DURATION_FOR_SENTENCE = dfc22_parameters.UncertainRange(1, 2)

DEFAULT_UNCERTAIN_REST_DURATION_FOR_PARAGRAPH = dfc22_parameters.UncertainRange(2, 3)

DEFAULT_UNCERTAIN_REST_DURATION_FOR_PAGE = dfc22_parameters.UncertainRange(3, 13)

del dfc22_parameters
