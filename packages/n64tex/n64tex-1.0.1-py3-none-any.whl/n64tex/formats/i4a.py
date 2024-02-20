from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage

import numpy as np

from n64tex.formats.base import BaseImage


class I4AImage(BaseImage):
    """I4A Image format. Each pixel is 4 bits long and follow this format

    III A

    Where:
        I = Intensity from 0-7
        A = Alpha channel from 0-1

    This format is typically coupled with a colour to produce an image
    various shades of said colour
    """

    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, *args, **kwargs) -> "I4AImage":
        """Generate an I4AImage from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image

        Returns:
            I4AImage: I4AImage object
        """
        split_bytes = lambda x: ((x & 0xF0) >> 4, x & 0x0F)
        data_array = np.frombuffer(raw_bytes, dtype=">u1")
        data_array = np.array(np.ravel(np.column_stack(split_bytes(data_array))))
        data_array.resize((height, width), refcheck=False)
        return cls(data_array, width, height)

    def to_rgba(self, colour: tuple[int, int, int] = (255, 255, 255)) -> "RGBAImage":
        """Converts I4AImage to RGBAImage

        Args:
            colour (tuple[int, int, int]): Colour to tint the image. Defaults to (255, 255, 255)

        Returns:
            RGBAImage: Converted RGBAImage object
        """

        def i4a_to_rgba(i4a_value):
            nonlocal colour
            # TODO: I'm pretty sure there's an actual algorithm for this
            # Should find and use it
            intensity_value = i4a_value >> 1
            alpha_value = i4a_value % 2
            r = max(min(colour[0] * (intensity_value / 7), 255), 0)
            g = max(min(colour[1] * (intensity_value / 7), 255), 0)
            b = max(min(colour[2] * (intensity_value / 7), 255), 0)
            a = int(255 * alpha_value)
            return r, g, b, a

        i4a_data_array = self.data_array.copy()

        rgba_data_array = list()
        for pixel_row in i4a_data_array:
            for pixel_colour in pixel_row:
                rgba_data_array.append(i4a_to_rgba(pixel_colour))

        rgba_data_array = np.array(rgba_data_array, dtype=">u1")
        rgba_data_array = np.resize(rgba_data_array, (self.height, self.width, 4))

        from n64tex.formats.rgba import RGBAImage

        return RGBAImage(rgba_data_array, self.width, self.height)
