import os
import unittest

from PIL import Image

from mutwo import dfc22_converters
from mutwo import dfc22_parameters


class ImageToEncodedImageTest(unittest.TestCase):
    def test_convert(self):
        dummy_sign_path = "tests/converters/dummy_signs"
        sign_sequence = [
            dfc22_parameters.SignElement(
                Image.open(f"{dummy_sign_path}/{image_path}"), []
            )
            for image_path in os.listdir(dummy_sign_path)
        ]
        image_to_encoded_image = dfc22_converters.ImageToEncodedImage(
            sign_sequence,
            contrast_factor=3,
            inverse=True,
        )
        image_to_convert = Image.open("tests/converters/queen.jpg")
        converted_image = image_to_encoded_image.convert(image_to_convert)
        converted_image_path = "tests/converters/queen_converted.jpg"
        converted_image.save(converted_image_path)

        self.assertTrue(os.path.exists(converted_image_path))


if __name__ == "__main__":
    unittest.main()
