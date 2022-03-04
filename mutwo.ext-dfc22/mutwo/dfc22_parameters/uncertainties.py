"""Initiate objects with uncertainties"""

import abc
import typing

import numpy as np
import ranges

from mutwo import core_utilities
from mutwo import dfc22_parameters


__all__ = (
    "resolve",
    "UncertainElement",
    "UncertainSequence",
    "UncertainSet",
    "UncertainDict",
    "UncertainRange",
    "UncertainCallable",
    "ResolutionStrategy",
    "RandomResolutionStrategy",
    "RandomChoice",
    "WeightedChoice",
    "RandomDistribution",
    "ConvertToSequence",
    "UncertainLetterElement",
    "UncertainPolygon",
    "UncertainIsSideActiveSequence",
    "UncertainTriangle",
    "UncertainQuad",
    "UncertainPentagon",
    "UncertainHexagon",
    "UncertainCircle",
    "UncertainLetter",
)


def resolve(object_to_resolve: typing.Any):
    return core_utilities.call_function_except_attribute_error(
        lambda object_to_resolve: object_to_resolve.resolve(),
        object_to_resolve,
        # In case the object doesn't have a resolve method,
        # it is not an instance of `UncertainElement`.
        # Therefore there is nothing to resolve and we
        # can just return the object.
        object_to_resolve,
    )


class UncertainElement(abc.ABC):
    @abc.abstractmethod
    def resolve(self) -> typing.Any:
        raise NotImplementedError


class ResolutionStrategy(abc.ABC):
    @abc.abstractmethod
    def __call__(self, uncertain_element_to_resolve: UncertainElement) -> typing.Any:
        raise NotImplementedError


class UncertainSequence(UncertainElement, list):
    """A sequence filled with :class:`UncertainElement`.

    When resolved it will return a sequence of type `resolution_type` where
    each child object has been resolved.
    """

    def __init__(self, iterable: typing.Iterable, resolution_type: typing.Type = list):
        super().__init__(iterable)
        self.resolution_type = resolution_type

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self[:]}, "
            f"resolution_type={self.resolution_type.__name__})"
        )

    def resolve(self) -> typing.Any:
        return self.resolution_type(
            [resolve(object_to_resolve) for object_to_resolve in self]
        )


class UncertainElementWithResolutionStrategy(UncertainElement):
    def __init__(self, resolution_strategy: ResolutionStrategy):
        self.resolution_strategy = resolution_strategy

    def resolve(self) -> typing.Any:
        return self.resolution_strategy(self)


class UncertainSet(UncertainElementWithResolutionStrategy, list):
    # Inherit from list and not from list to avoid removing
    # duplicates.

    def __init__(
        self,
        iterable: typing.Iterable,
        resolution_strategy: typing.Optional[ResolutionStrategy] = None,
    ):
        if resolution_strategy is None:
            resolution_strategy = RandomChoice()
        list.__init__(self, iterable)
        UncertainElementWithResolutionStrategy.__init__(self, resolution_strategy)

    def resolve(self) -> typing.Any:
        return self.resolution_strategy(
            [resolve(object_to_resolve) for object_to_resolve in self]  # type: ignore
        )


class UncertainDict(UncertainElementWithResolutionStrategy, dict):
    def __init__(
        self,
        # object -> likelihood pairs
        dictionary: dict[typing.Any, float],
        resolution_strategy: typing.Optional[ResolutionStrategy] = None,
        **kwargs,
    ):
        if resolution_strategy is None:
            resolution_strategy = WeightedChoice()
        dict.__init__(self, dictionary, **kwargs)
        UncertainElementWithResolutionStrategy.__init__(self, resolution_strategy)

    def resolve(self) -> typing.Any:
        return self.resolution_strategy(
            {resolve(object_to_resolve): likelihood for object_to_resolve, likelihood in self.items()}  # type: ignore
        )


class UncertainRange(UncertainElementWithResolutionStrategy, ranges.Range):
    def __init__(
        self,
        *args,
        resolution_strategy: typing.Optional[ResolutionStrategy] = None,
        **kwargs,
    ):
        if resolution_strategy is None:
            resolution_strategy = RandomDistribution()
        ranges.Range.__init__(self, *args, **kwargs)
        UncertainElementWithResolutionStrategy.__init__(self, resolution_strategy)


class UncertainCallable(UncertainElement):
    def __init__(self, callable_object: typing.Callable, **argument_for_callable):
        self.callable_object = callable_object
        self._argument_for_callable_dict = argument_for_callable

    @staticmethod
    def _assign_arguments_to_new_class(
        new_class: typing.Type, argument_for_callable: dict[str, typing.Any]
    ):
        for argument_name in argument_for_callable.keys():

            def getter(self) -> typing.Any:
                return resolve(self.get_argument(argument_name))

            def setter(self, new_value: typing.Any):
                self.set_argument(argument_name, new_value)

            setattr(
                new_class,
                argument_name,
                property(
                    fget=getter,
                    fset=setter,
                ),
            )

    @classmethod
    def from_class(
        cls,
        callable_object: typing.Callable,
        class_to_mimic: typing.Optional[typing.Type] = None,
        **argument_for_callable,
    ):
        if class_to_mimic is None:
            class_to_mimic = callable_object

        assert isinstance(class_to_mimic, type)

        name = f"Uncertain{class_to_mimic.__name__}"

        def init(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)

        def __str__(self) -> str:
            return f"{name}({self.argument_to_resolvable_object_dict})"

        new_class = type(
            name,
            (cls, class_to_mimic),  # type: ignore
            {
                "__init__": init,
                "__str__": __str__,
                "__repr__": __str__,
            },
        )

        cls._assign_arguments_to_new_class(new_class, argument_for_callable)

        return new_class(callable_object, **argument_for_callable)  # type: ignore

    @property
    def argument_to_resolvable_object_dict(
        self,
    ) -> dict[str, typing.Union[typing.Any, UncertainElement]]:
        return self._argument_for_callable_dict

    @property
    def argument_to_resolution_dict(self) -> dict[str, typing.Any]:
        argument_to_resolution = {}
        for (
            argument,
            object_to_resolve,
        ) in self.argument_to_resolvable_object_dict.items():
            resolution = resolve(object_to_resolve)
            argument_to_resolution.update({argument: resolution})
        return argument_to_resolution

    def set_argument(self, name: str, value: typing.Any):
        self.argument_to_resolvable_object_dict[name] = value

    def get_argument(self, name: str) -> typing.Any:
        return self.argument_to_resolvable_object_dict[name]

    def resolve(self, **kwargs) -> typing.Any:
        return self.callable_object(**dict(self.argument_to_resolution_dict, **kwargs))


class RandomResolutionStrategy(ResolutionStrategy):
    def __init__(self, seed: int = 100):
        self._random = np.random.default_rng(seed)


class RandomChoice(RandomResolutionStrategy):
    def __call__(self, uncertain_element_to_resolve: UncertainSet) -> typing.Any:
        n_items = len(uncertain_element_to_resolve)
        average_value = 1 / n_items
        probability_tuple = tuple(average_value for _ in range(n_items))
        return self._random.choice(
            a=tuple(uncertain_element_to_resolve), p=probability_tuple, size=1
        )[0]


class WeightedChoice(RandomResolutionStrategy):
    def __call__(
        self, uncertain_element_to_resolve: dict[typing.Any, float]
    ) -> typing.Any:
        item_tuple = tuple(uncertain_element_to_resolve.keys())
        probability_tuple = core_utilities.scale_sequence_to_sum(
            tuple(uncertain_element_to_resolve.values()), 1
        )
        return self._random.choice(a=item_tuple, p=probability_tuple, size=1)[0]  # type: ignore


class RandomDistribution(RandomResolutionStrategy):
    def __init__(self, *args, distribution_name: str = "uniform", **kwargs):
        super().__init__(*args, **kwargs)
        self.distribution_name = distribution_name

    def __call__(self, uncertain_element_to_resolve: UncertainRange) -> typing.Any:
        start, end = (
            uncertain_element_to_resolve.start,
            uncertain_element_to_resolve.end,
        )
        return getattr(self._random, self.distribution_name)(start, end, size=1)[0]


class ConvertToSequence(ResolutionStrategy):
    def __init__(self, sequence_type: typing.Type = list):
        self._sequence_type = sequence_type

    def __call__(self, uncertain_element_to_resolve: UncertainSet) -> typing.Any:
        return self._sequence_type(uncertain_element_to_resolve)


class UncertainLetterElement(UncertainCallable):
    def __init__(
        self,
        letter_element_constructor: typing.Callable,
        thickness=UncertainRange(4, 30),
        x_displacement=UncertainRange(-0.75, 0.75),
        y_displacement=UncertainRange(-0.75, 0.75),
        **argument_for_callable,
    ):
        super().__init__(
            letter_element_constructor,
            x_displacement=x_displacement,
            y_displacement=y_displacement,
            thickness=thickness,
            **argument_for_callable,
        )


class UncertainIsSideActiveSequence(UncertainSequence):
    pass


class UncertainPolygon(UncertainLetterElement):
    def __init__(
        self,
        is_side_active_sequence=None,
        round_corner_strength_sequence=None,
        max_length=None,
        angle_proportion_sequence=None,
        length_proportion_sequence=None,
        rotation_angle=None,
        **kwargs,
    ):
        if not is_side_active_sequence:
            is_side_active_sequence = UncertainIsSideActiveSequence(
                [UncertainSet([True, False]) for _ in range(self.polygon_class.n_sides)]
            )
        if not round_corner_strength_sequence:
            round_corner_strength_sequence = UncertainSequence(
                [UncertainRange(0, 0.5) for _ in range(self.polygon_class.n_sides)]
            )
        if not max_length:
            max_length = UncertainRange(0.25, 0.75)
        if not angle_proportion_sequence:
            angle_proportion_sequence = UncertainSequence(
                [UncertainRange(0.5, 2) for _ in range(self.polygon_class.n_sides)]
            )
        if not length_proportion_sequence:
            length_proportion_sequence = UncertainSequence(
                [UncertainRange(0.5, 2) for _ in range(self.polygon_class.n_sides - 2)]
            )
        if not rotation_angle:
            rotation_angle = UncertainRange(0, 90)
        super().__init__(
            self.polygon_class.from_angles_and_lengths,
            is_side_active_sequence=is_side_active_sequence,
            round_corner_strength_sequence=round_corner_strength_sequence,
            max_length=max_length,
            angle_proportion_sequence=angle_proportion_sequence,
            length_proportion_sequence=length_proportion_sequence,
            rotation_angle=rotation_angle,
            **kwargs,
        )

    @classmethod
    @property
    def polygon_class(cls) -> typing.Type[dfc22_parameters.Polygon]:
        raise NotImplementedError


class UncertainTriangle(UncertainPolygon):
    @classmethod
    @property
    def polygon_class(cls) -> typing.Type[dfc22_parameters.Polygon]:
        return dfc22_parameters.Triangle


class UncertainQuad(UncertainPolygon):
    @classmethod
    @property
    def polygon_class(cls) -> typing.Type[dfc22_parameters.Polygon]:
        return dfc22_parameters.Quad


class UncertainPentagon(UncertainPolygon):
    @classmethod
    @property
    def polygon_class(cls) -> typing.Type[dfc22_parameters.Polygon]:
        return dfc22_parameters.Pentagon


class UncertainHexagon(UncertainPolygon):
    @classmethod
    @property
    def polygon_class(cls) -> typing.Type[dfc22_parameters.Polygon]:
        return dfc22_parameters.Hexagon


class UncertainCircle(UncertainLetterElement):
    def __init__(
        self,
        activity_tuple_sequence=((True, 1),),
        radius_proportion=UncertainRange(0.2, 0.45),
        **kwargs,
    ):
        super().__init__(
            dfc22_parameters.Circle,
            activity_tuple_sequence=activity_tuple_sequence,
            radius_proportion=radius_proportion,
            **kwargs,
        )


class UncertainLetter(UncertainCallable):
    def __init__(
        self,
        letter_canvas: dfc22_parameters.LetterCanvas = dfc22_parameters.LetterCanvas(),
        uncertain_letter_element_sequence: typing.Sequence[UncertainLetterElement] = [
            UncertainCircle(),
            UncertainQuad(),
            UncertainTriangle(),
            UncertainCircle(),
        ],
    ):
        super().__init__(
            dfc22_parameters.Letter,
            letter_canvas=letter_canvas,
            letter_element_list=UncertainSet(
                uncertain_letter_element_sequence,
                resolution_strategy=ConvertToSequence(list),
            ),
        )
