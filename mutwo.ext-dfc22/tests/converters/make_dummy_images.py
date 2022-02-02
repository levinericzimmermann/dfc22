"""Script to render dummy images to be used for tests"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

if __name__ == "__main__":
    text_tuple = (
        ".",
        " ",
        "@",
        "-",
        "`",
        "'",
        "+",
        "=",
        ",",
        ";",
        "|",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    )
    image_size = (30, 30)
    image_mode = "L"
    # font = ImageFont.load("dummy_font/Junicode-Bold.ttf")
    font = ImageFont.truetype("dummy_font/Junicode.ttf", size=30)

    path = "dummy_signs"

    for nth_text, text in enumerate(text_tuple):
        img = Image.new(image_mode, image_size, color=255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=font)
        img.save(f"{path}/{nth_text}.jpg")
