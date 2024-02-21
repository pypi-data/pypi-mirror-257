from typing import Tuple

from PIL import Image


def resize_image(image: Image.Image, resize: Tuple[int, int]) -> Image.Image:
    """
    Resize an image to the desired dimensions

    :param image: The image to resize.
    :param resize:  New size of the map section is a tuple (width, height) or (None, height) or (None, width).
    If both are provided, the aspect ratio may be distorted. If only one is provided, the original aspect ratio is
    maintained. If both are None, the original size is used.
    :return: The resized image.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("The image must be a PIL Image object!")

    original_width, original_height = image.size

    if original_width == 0 or original_height == 0:
        raise ValueError("The image has dimensions of 0x0 pixels, which cannot be resized.")

    desired_width, desired_height = resize

    if desired_width is None and desired_height is None:
        return image

    if desired_width is None:
        desired_width = int(desired_height * original_width / original_height)
    elif desired_height is None:
        desired_height = int(desired_width * original_height / original_width)

    new_size = (desired_width, desired_height)
    resized_image = image.resize(new_size, Image.LANCZOS)

    return resized_image
