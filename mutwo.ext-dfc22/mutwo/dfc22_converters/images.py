"""Transform images"""

import typing

import numpy as np
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps

from mutwo import core_converters
from mutwo import core_utilities
from mutwo import dfc22_parameters


__all__ = ("ImageToEncodedImage",)


class GrayScalePixelToBrightness(core_converters.abc.Converter):
    MAXIMUM_PIXEL_VALUE = 255

    def convert(self, grayscale_pixel: int) -> float:
        return grayscale_pixel / self.MAXIMUM_PIXEL_VALUE


class ImageToBrightness(core_converters.abc.Converter):
    def convert(self, image_to_convert: Image.Image) -> float:
        image_as_grayscale = ImageOps.grayscale(image_to_convert)
        average_grayscale_value = np.average(image_as_grayscale.getdata())
        return GrayScalePixelToBrightness().convert(average_grayscale_value)


class ImageToEncodedImage(core_converters.abc.Converter):
    ImageGrid = list[list[Image.Image]]

    # For mode see:
    # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
    # "L (8-bit pixels, black and white)"
    IMAGE_MODE = "L"

    def __init__(
        self,
        sign_sequence: typing.Sequence[dfc22_parameters.abc.Sign],
        # How much bigger one pixel will become after encoding it
        pixel_resize_factor_tuple: tuple[int, int] = (30, 30),
        resize_image_width: int = 100,
        contrast_factor: float = 2,
        inverse: bool = False,
    ):
        self._contrast_factor = contrast_factor
        self._sign_sequence = sign_sequence
        self._n_signs = len(self._sign_sequence)
        self._brightness_tuple = tuple(
            ImageToBrightness().convert(sign.image) for sign in sign_sequence
        )
        self._resized_image_tuple = tuple(
            sign.image.resize(pixel_resize_factor_tuple) for sign in self._sign_sequence
        )
        self._sorted_brightness_tuple = tuple(sorted(self._brightness_tuple))
        self._pixel_resize_factor_tuple = pixel_resize_factor_tuple
        self._resize_image_width = resize_image_width
        self._empty_image = Image.new(
            self.IMAGE_MODE, pixel_resize_factor_tuple, color=255
        )
        self._inverse = inverse

    def _brightness_to_scaled_image(self, brightness: float) -> Image.Image:
        index = self._brightness_tuple.index(
            self._sorted_brightness_tuple[
                int(core_utilities.scale(brightness, 0, 1, 0, self._n_signs - 1))
            ]
        )
        return self._resized_image_tuple[index]

    def _image_to_image_grid(self, image_as_grayscale: Image.Image) -> ImageGrid:
        image_grid = [
            [self._empty_image for _ in range(image_as_grayscale.width)]
            for _ in range(image_as_grayscale.height)
        ]
        for x_position in range(image_as_grayscale.width):
            for y_position in range(image_as_grayscale.height):
                pixel = image_as_grayscale.getpixel((x_position, y_position))
                brightness = GrayScalePixelToBrightness().convert(pixel)
                image = self._brightness_to_scaled_image(brightness)
                image_grid[y_position][x_position] = image
        return image_grid

    def _image_grid_to_image(
        self, image_grid: ImageGrid, max_x: int, max_y: int
    ) -> Image.Image:
        x_factor, y_factor = self._pixel_resize_factor_tuple
        new_size = (max_x * x_factor, max_y * y_factor)
        image_blueprint = Image.new(mode=self.IMAGE_MODE, size=new_size, color=255)
        for nth_row, row in enumerate(image_grid):
            for nth_column, image in enumerate(row):
                position = (nth_column * x_factor, nth_row * y_factor)
                image_blueprint.paste(image, position)
        return image_blueprint

    def _resize_image_to_convert(self, image_to_convert: Image.Image) -> Image.Image:
        resize_image_width = self._resize_image_width
        image_scale_factor = resize_image_width / image_to_convert.width
        resize_image_height = int(image_to_convert.height * image_scale_factor)
        resized_image = image_to_convert.resize(
            (resize_image_width, resize_image_height)
        )
        return resized_image

    def _inverse_image_to_convert(self, image_to_convert: Image.Image) -> Image.Image:
        if self._inverse:
            return ImageOps.invert(image_to_convert)
        return image_to_convert

    def _adjust_image_contrast(self, image_to_convert: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Contrast(image_to_convert)
        enhanced_image = enhancer.enhance(self._contrast_factor)
        return enhanced_image

    def convert(self, image_to_convert: Image.Image) -> Image.Image:
        resized_image = self._resize_image_to_convert(
            self._adjust_image_contrast(
                self._inverse_image_to_convert(image_to_convert)
            )
        )
        image_as_grayscale = ImageOps.grayscale(resized_image)
        image_grid = self._image_to_image_grid(image_as_grayscale)
        image = self._image_grid_to_image(
            image_grid, resized_image.width, resized_image.height
        )
        return image
