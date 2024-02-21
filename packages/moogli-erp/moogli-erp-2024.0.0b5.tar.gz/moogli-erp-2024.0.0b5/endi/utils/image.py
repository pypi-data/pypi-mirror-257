"""
    utilities for image handling
"""
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from io import BytesIO
from endi.utils.sys_environment import resource_filename


def ensure_rgb(image):
    """
    Ensure the image is in RGB format
    """
    if image.mode == "RGBA":
        # required for the split
        image.load()
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")
    return image


class ImageRatio:
    """
    Ensure images respect the given proportions by adding white spaces

    r = ImageRatio(height_proportion, width_proportion, default_color)
    resized_image_buffer = r.complete(image_buffer)

    resized_image_buffer will respect the given proportions and
    will be filed with the given color


    height

        The destination height used to compile the dest ratio

    width

        The destination width used to compile the dest ratio

    color

        The RGB tuple describing the filling color to use
    """

    def __init__(
        self,
        width,
        height,
        color=(
            255,
            255,
            255,
        ),
    ):
        self.proportions = float(width) / float(height)
        self.color = color

    def get_white_layer(self, width, height):
        """
        Returns a white layer that will be our image background
        """
        size = (width, height)
        return Image.new("RGB", size, self.color)

    def complete(self, img_buf):
        """
        Complete the image to get at last my proportions, not more
        """
        img_buf.seek(0)
        img_obj = Image.open(img_buf)
        img_obj = ensure_rgb(img_obj)

        width, height = img_obj.size
        img_proportions = float(width) / float(height)

        if img_proportions >= self.proportions:
            mybuffer = BytesIO()
            img_obj.save(mybuffer, format="PNG", mode="RGB")
            mybuffer.seek(0)
            return mybuffer
        else:
            new_width = int(height * self.proportions)
            new_height = height
            padding = int((new_width - width) / 2)
            layer = self.get_white_layer(new_width, new_height)
            layer.paste(img_obj, (padding, 0))
            mybuffer = BytesIO()
            layer.save(mybuffer, format="PNG")
            mybuffer.seek(0)
            return mybuffer


class ImageResizer:
    """
    Ensure image fit inside the given box

    if the image's width or height are larger than the provided one, the image
    is resized accordingly
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def complete(self, img_buf):
        result = img_buf
        result.seek(0)
        img_obj = Image.open(result)
        img_obj = ensure_rgb(img_obj)
        width, height = img_obj.size

        img_obj.thumbnail((self.width, self.height), Image.ANTIALIAS)
        result = BytesIO()
        img_obj.save(result, format="PNG")
        result.seek(0)
        return result


def build_header(text, size=(1000, 250)):
    """
    Build a header image containing text

    :param str text: The text to write
    :returns: The header image
    :rtype: BytesIO instance populated with the image datas in PNG Format
    """
    img = Image.new("RGB", size, (255, 255, 255))
    fontpath = resource_filename("static/fonts/playfair_display_regular.ttf")
    font = ImageFont.truetype(fontpath, 30)

    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=font, fill=(0, 0, 0))
    mybuffer = BytesIO()
    img.save(mybuffer, "PNG")
    mybuffer.seek(0)
    return mybuffer
