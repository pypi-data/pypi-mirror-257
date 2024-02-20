from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage

import numpy as np

from n64tex.formats.base import BaseImage


class I8AImage(BaseImage):
    """I8A Image format. Each pixel is 8 bits long and follow this format

    IIII AAAA

    Where:
        I = Intensity from 0-255
        A = Alpha channel from 0-15

    This format is typically coupled with a colour to produce an image
    various shades of said colour
    """

    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, *args, **kwargs) -> "I8AImage":
        """Generate an I8AImage from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image

        Returns:
            I8AImage: I8AImage object
        """
        data_array = np.frombuffer(raw_bytes, dtype=">u1")
        data_array = np.array(data_array)
        data_array.resize((height, width), refcheck=False)
        return cls(data_array, width, height)

    def to_rgba(self, colour: tuple[int, int, int] = (255, 255, 255)) -> "RGBAImage":
        """Converts I8AImage to RGBAImage

        Args:
            colour (tuple[int, int, int]): Colour to tint the image. Defaults to (255, 255, 255)

        Returns:
            RGBAImage: Converted RGBAImage object
        """

        def i8a_to_rgba(i8a_value):
            nonlocal colour
            # TODO: I'm pretty sure there's an actual algorithm for this
            # Should find and use it
            intensity_value = i8a_value >> 4
            alpha_value = i8a_value % 16
            r = max(min(colour[0] * (intensity_value / 15), 255), 0)
            g = max(min(colour[1] * (intensity_value / 15), 255), 0)
            b = max(min(colour[2] * (intensity_value / 15), 255), 0)
            a = int(255 * (alpha_value / 15))
            return r, g, b, a

        i8a_data_array = self.data_array.copy()

        rgba_data_array = list()
        for pixel_row in i8a_data_array:
            for pixel_colour in pixel_row:
                rgba_data_array.append(i8a_to_rgba(pixel_colour))

        rgba_data_array = np.array(rgba_data_array, dtype=">u1")
        rgba_data_array = np.resize(rgba_data_array, (self.height, self.width, 4))

        from n64tex.formats.rgba import RGBAImage

        return RGBAImage(rgba_data_array, self.width, self.height)
