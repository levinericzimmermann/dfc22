import dataclasses

from PIL import Image
from PIL import ImageOps

from mutwo import core_converters
from mutwo import dfc22_parameters

__all__ = (
    "PaperCanvas",
    "LetterTupleToImage",
)


@dataclasses.dataclass
class PaperCanvas(object):
    x: int = 3000
    y: int = 4000


class LetterTupleToImage(core_converters.abc.Converter):
    def __init__(
        self,
        paper_canvas: PaperCanvas = PaperCanvas(),
        x_margin: float = 250,
        y_margin: float = 100,
        x_whitespace: float = -30,
        y_whitespace: float = 35,
        letter_height: float = 200,
        background_color: str = "white",
    ):
        self._paper_canvas = paper_canvas
        self._x_margin = x_margin
        self._y_margin = y_margin
        self._x_whitespace = x_whitespace
        self._y_whitespace = y_whitespace
        self._letter_height = letter_height
        self._max_x = self._paper_canvas.x - self._x_margin
        self._background_color = background_color

    def _scale_letter_image(self, letter_image_to_scale: Image.Image) -> Image.Image:
        image_height = letter_image_to_scale.height
        factor = self._letter_height / image_height
        return ImageOps.scale(letter_image_to_scale, factor)

    def convert(
        self, letter_tuple_to_convert: tuple[dfc22_parameters.Letter, ...], path: str
    ):
        image = Image.new(
            "RGBA",
            (self._paper_canvas.x, self._paper_canvas.y),
            color=self._background_color,
        )
        current_x, current_y = self._x_margin, self._y_margin
        for letter in letter_tuple_to_convert:
            scaled_letter_image = self._scale_letter_image(letter.image)
            if scaled_letter_image.width + current_x >= self._max_x:
                current_x = self._x_margin
                current_y += self._letter_height + self._y_whitespace
            image.paste(scaled_letter_image, (current_x, current_y))
            current_x += self._x_whitespace + scaled_letter_image.width
        image.save(path)
