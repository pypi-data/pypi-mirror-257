from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage

import numpy as np

from n64tex.formats.base import BaseImage


class RGBA5551Image(BaseImage):
    """RGBA5551 Image format. Each pixel is 16 bits long and follow this format

    RRRRR GGGGG BBBBB A

    Where:
        R = Red channel from 0-31
        G = Green channel from 0-31
        B = Blue channel from 0-31
        A = Alpha channel from 0-1
    """

    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, *args, **kwargs) -> "RGBA5551Image":
        """Generate an RGBA5551Image from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image

        Returns:
            RGBA5551Image: RGBA5551Image object
        """
        data_array = np.frombuffer(raw_bytes, dtype=">u2")
        data_array = np.array(data_array)
        data_array.resize((height, width), refcheck=False)
        return cls(data_array, width, height)

    def to_rgba(self) -> "RGBAImage":
        """Converts RGBA5551Image to RGBAImage

        Returns:
            RGBAImage: Converted RGBAImage object
        """

        def rgba5551_to_rgba(rgba5551_value):
            r = (rgba5551_value & 0xF800) >> 8
            g = (rgba5551_value & 0x7C0) >> 3
            b = (rgba5551_value & 0x3E) << 2
            a = 255 if rgba5551_value & 0x1 else 0
            return r, g, b, a

        rgba_5551_data_array = self.data_array.copy()
        rgba_5551_data_array = rgba_5551_data_array.astype(np.uint16)

        rgba_data_array = list()
        if len(rgba_5551_data_array.shape) == 1:
            for pixel_colour in rgba_5551_data_array:
                rgba_data_array.append(rgba5551_to_rgba(pixel_colour))
        else:
            for pixel_row in rgba_5551_data_array:
                for pixel_colour in pixel_row:
                    rgba_data_array.append(rgba5551_to_rgba(pixel_colour))

        rgba_data_array = np.array(rgba_data_array, dtype=">u1")
        rgba_data_array = np.resize(rgba_data_array, (self.height, self.width, 4))

        from n64tex.formats.rgba import RGBAImage

        return RGBAImage(rgba_data_array, self.width, self.height)
