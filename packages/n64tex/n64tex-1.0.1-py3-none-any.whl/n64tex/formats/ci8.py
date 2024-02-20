import pathlib

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage

import numpy as np

from n64tex.formats.base import BaseImage

class CI8Image(BaseImage):
    """CI8 Image format. Each pixel is 4 bits long, which are pointers to an array of RGBA5551 colours
       The palette can only have 255 colours
    
    The image follows this format:
    
    PPPPPPPP
    
    Where: 
        P = Address of colour in RGBA5551 array
        
    
    The RGBA5551 array (colour palette) follows this format:
    
    RRRRR GGGGG BBBBB A

    Where:
        R = Red channel from 0-31
        G = Green channel from 0-31
        B = Blue channel from 0-31
        A = Alpha channel from 0-1
    """
    
    def __init__(self, data_array: np.array, width: int, height: int, palette: np.array = None):
        """Initializer that takes in Numpy array, width, and height. This
           shouldn't be called directly unless you know what you're doing.
           Instead, you should call either the `from_image` or `from_bytes`
           class methods. Can optionally take a palette array for CI images

        Args:
            data_array (np.array): Numpy array
            width (int): Width of image
            height (int): Height of image
            palette (np.array, optional): Colour palette to use with this image. Defaults to None.
        """
        assert palette is not None, "A palette is required for CI8 Images"
        assert 256 >= len(palette) >= 1, f"CI8 Images can only support a palette of 255 colours.\nPalette has {len(palette)} colours"
        super().__init__(data_array, width, height, palette)
    
    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, palette_bytes: bytes) -> "CI8Image":
        """Generate an CI8Image from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image
            palette_bytes (bytes): Colour palette bytes to use with this image

        Returns:
            CI8Image: CI8Image object
        """
        # Image pointers
        if len(raw_bytes) == 2720:
            import pudb; pu.db
        data_array = np.frombuffer(raw_bytes, dtype=">u1")
        data_array = np.array(data_array)
        data_array.resize((height, width), refcheck=False)
        
        # Image palette
        assert palette_bytes, "CI8 images require a palette to function"
        palette = np.frombuffer(palette_bytes, dtype=">u2")
        
        return cls(data_array, width, height, palette)
    
    def to_rgba(self) -> "RGBAImage":
        """Converts CI8Image to RGBAImage

        Returns:
            RGBAImage: Converted RGBAImage object
        """

        def rgba5551_to_rgba(rgba5551_value):
            r = (rgba5551_value & 0xF800) >> 8
            g = (rgba5551_value & 0x7C0) >> 3
            b = (rgba5551_value & 0x3E) << 2
            a = 255 if rgba5551_value & 0x1 else 0
            return r, g, b, a
        
        rgba_5551_data_array = self.palette.copy()

        palette_data_array = list()
        for pixel_colour in rgba_5551_data_array:
            palette_data_array.append(rgba5551_to_rgba(pixel_colour))
                
        rgba_data_array = list()
        for pointer in self.data_array.flatten():
            # try:
            rgba_data_array.append(palette_data_array[pointer])
            # except:
                # import pudb; pu.db
            
        rgba_data_array = np.array(rgba_data_array, dtype=">u1")
        rgba_data_array = np.resize(rgba_data_array, (self.height, self.width, 4))
        
        from n64tex.formats.rgba import RGBAImage

        return RGBAImage(rgba_data_array, self.width, self.height, self.palette)
    
    def save(self, filename: str, save_palette: bool = False):
        """Saves Object to a file using PIL along with the palette

        Args:
            filename (str): Filename to save to
            save_palette (bool): Whether to save the palette or not. Defaults to False
        """
        if save_palette:
            from n64tex.formats import RGBA5551Image
            filepath = pathlib.Path(filename)
            palette = RGBA5551Image.from_bytes(self.palette.astype('>u2').tobytes(), 16, 16)
            palette.save(filepath.parent / f'palette_{filepath.name}')
        super().save(filename)