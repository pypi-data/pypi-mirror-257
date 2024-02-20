from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBA5551Image, I4Image, I8Image, I4AImage, I8AImage, CI4Image, CI8Image

import numpy as np

from n64tex.formats.base import BaseImage, T


class RGBAImage(BaseImage):
    """RGBA Image format. Each pixel is 32 bits long and follow this format

    RRRRRRRR GGGGGGGG BBBBBBBB AAAAAAAA

    Where:
        R = Red channel from 0-255
        G = Green channel from 0-255
        B = Blue channel from 0-255
        A = Alpha channel from 0-255
    """

    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, *args, **kwargs) -> "RGBAImage":
        """Generate an RGBAImage from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image

        Returns:
            RGBAImage: RGBAImage object
        """
        data_array = np.frombuffer(raw_bytes, dtype=">u1")
        data_array = np.array(data_array)
        data_array.resize((height, width, 4), refcheck=False)
        return cls(data_array, width, height)

    def convert_to(self, cls: T) -> T:
        from n64tex.formats import RGBA5551Image, I4Image, I8Image, I4AImage, I8AImage, CI4Image, CI8Image

        CONVERTERS = {
            RGBAImage: lambda: self,
            RGBA5551Image: self.to_rgba5551,
            I4Image: self.to_i4,
            I4AImage: self.to_i4a,
            I8Image: self.to_i8,
            I8AImage: self.to_i8a,
            CI4Image: self.to_ci4,
            CI8Image: self.to_ci8,
        }
        return CONVERTERS[cls]()

    def to_rgba5551(self) -> "RGBA5551Image":
        """Converts RGBAImage to RGBA5551Image

        Returns:
            RGBA5551Image: Converted RGBA5551Image object
        """

        def rgba_to_rgba5551(rgba_value):
            rgba_value[0] = (rgba_value[0] >> 3) << 11
            rgba_value[1] = (rgba_value[1] >> 3) << 6
            rgba_value[2] = (rgba_value[2] >> 3) << 1
            rgba_value[3] = 1 if rgba_value[3] > 0 else 0

        rgba_5551_data_array = self.data_array.copy()
        rgba_5551_data_array = rgba_5551_data_array.astype(np.uint16)

        for pixel_row in rgba_5551_data_array:
            for pixel_colour in pixel_row:
                rgba_to_rgba5551(pixel_colour)

        rgba_5551_data_array = np.sum(rgba_5551_data_array, axis=2)
        rgba_5551_data_array = rgba_5551_data_array.astype(np.uint16)

        from n64tex.formats.rgba5551 import RGBA5551Image

        return RGBA5551Image(rgba_5551_data_array, self.width, self.height)

    def to_i4(self) -> "I4Image":
        """Converts RGBAImage to I4Image

        Returns:
            I4Image: Converted I4Image object
        """
        reduce_bytes = lambda x: x / 17

        i4_data_array = self.data_array.copy()
        i4_data_array = np.average(i4_data_array, axis=2)
        i4_data_array = reduce_bytes(i4_data_array)
        i4_data_array = np.round(i4_data_array).astype(np.uint8)

        from n64tex.formats.i4 import I4Image

        return I4Image(i4_data_array, self.width, self.height)
    
    def to_i4a(self) -> "I4AImage":
        """Converts RGBAImage to I4AImage

        Returns:
            I4Image: Converted I4AImage object
        """
        # ! It's likely that this is incorrect. A second set of eyes is necessary
        reduce_bytes = lambda x: x / 17

        i4a_data_array = self.data_array.copy()
        i4a_data_array = np.average(i4a_data_array, axis=2)
        i4a_data_array = reduce_bytes(i4a_data_array)
        i4a_data_array = np.round(i4a_data_array).astype(np.uint8)

        from n64tex.formats.i4a import I4AImage

        return I4AImage(i4a_data_array, self.width, self.height)

    def to_i8(self) -> "I8Image":
        """Converts RGBAImage to I8Image

        Returns:
            I8Image: Converted I8Image object
        """
        i8_data_array = self.data_array.copy()
        i8_data_array = np.average(i8_data_array, axis=2).astype(np.uint8)

        from n64tex.formats.i8 import I8Image

        return I8Image(i8_data_array, self.width, self.height)

    def to_i8a(self) -> "I8AImage":
        """Converts RGBAImage to I8AImage

        Returns:
            I8AImage: Converted I8AImage object
        """
        i8a_data_array = self.data_array.copy()
        i8a_data_array = np.average(i8a_data_array, axis=2).astype(np.uint8)

        from n64tex.formats.i8a import I8AImage

        return I8AImage(i8a_data_array, self.width, self.height)
    
    def to_ci4(self) -> "CI4Image":
        """Converts RGBAImage to CI4Image

        Returns:
            CI4Image: Converted CI4Image object
        """
        
        def rgba_to_rgba5551(rgba_value):
            rgba_value[0] = (rgba_value[0] >> 3) << 11
            rgba_value[1] = (rgba_value[1] >> 3) << 6
            rgba_value[2] = (rgba_value[2] >> 3) << 1
            rgba_value[3] = 1 if rgba_value[3] > 0 else 0

        # Generate the Palette Array if it doesn't already exist
        if self.palette is not None:
            palette_data_array = self.palette.copy()
        else:
            palette_data_array = np.reshape(self.data_array, (-1, 4))
            palette_data_array = np.unique(palette_data_array, axis=0)
            
            palette_data_array = palette_data_array.astype(np.uint16)
            for pixel_colour in palette_data_array:
                rgba_to_rgba5551(pixel_colour)
            palette_data_array = np.sum(palette_data_array, axis=1)
            palette_data_array = np.unique(palette_data_array, axis=0)
            palette_data_array = palette_data_array.astype(np.uint16)

        # Generate the Pointer Array
        ci4_data_array = list()
        for pixel_colour in np.reshape(self.data_array, (-1, 4)).astype(np.uint16):
            rgba_to_rgba5551(pixel_colour)
            palette_index = np.where(palette_data_array == np.sum(pixel_colour))
            ci4_data_array.append(palette_index)
        
        ci4_data_array = np.array(ci4_data_array)
        ci4_data_array = np.resize(ci4_data_array, (self.height, self.width))
        ci4_data_array = ci4_data_array.astype(np.uint8)
            
        from n64tex.formats.ci4 import CI4Image

        return CI4Image(ci4_data_array, self.width, self.height, palette_data_array)
    
    def to_ci8(self) -> "CI8Image":
        """Converts RGBAImage to CI8Image

        Returns:
            CI8Image: Converted CI8Image object
        """
        
        def rgba_to_rgba5551(rgba_value):
            rgba_value[0] = (rgba_value[0] >> 3) << 11
            rgba_value[1] = (rgba_value[1] >> 3) << 6
            rgba_value[2] = (rgba_value[2] >> 3) << 1
            rgba_value[3] = 1 if rgba_value[3] > 0 else 0
            
        # Generate the Palette Array if it doesn't already exist
        if self.palette is not None:
            palette_data_array = self.palette.copy()
        else:
            palette_data_array = np.reshape(self.data_array, (-1, 4))
            palette_data_array = np.unique(palette_data_array, axis=0)
            
            palette_data_array = palette_data_array.astype(np.uint16)
            for pixel_colour in palette_data_array:
                rgba_to_rgba5551(pixel_colour)
            palette_data_array = np.sum(palette_data_array, axis=1)
            palette_data_array = np.unique(palette_data_array, axis=0)
            palette_data_array = palette_data_array.astype(np.uint16)
        
        # Generate the Pointer Array
        ci8_data_array = list()
        for pixel_colour in np.reshape(self.data_array, (-1, 4)).astype(np.uint16):
            rgba_to_rgba5551(pixel_colour)
            palette_index = np.where(palette_data_array == np.sum(pixel_colour))
            ci8_data_array.append(palette_index)
        ci8_data_array = np.array(ci8_data_array)
        ci8_data_array = np.resize(ci8_data_array, (self.height, self.width))
        ci8_data_array = ci8_data_array.astype(np.uint8)
            
        from n64tex.formats.ci8 import CI8Image

        return CI8Image(ci8_data_array, self.width, self.height, palette_data_array)