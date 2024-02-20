from enum import Enum

from typing import Union

from n64tex.formats.i4 import I4Image
from n64tex.formats.i4a import I4AImage
from n64tex.formats.i8 import I8Image
from n64tex.formats.i8a import I8AImage
from n64tex.formats.ci4 import CI4Image
from n64tex.formats.ci8 import CI8Image
from n64tex.formats.rgba import RGBAImage
from n64tex.formats.rgba5551 import RGBA5551Image


class Formats(Enum):
    i4 = I4Image
    i4a = I4AImage
    i8 = I8Image
    i8a = I8AImage
    ci4 = CI4Image
    ci8 = CI8Image
    rgba = RGBAImage
    rgba5551 = RGBA5551Image

    def __str__(self):
        return self.name
    
N64TextureFormat = Union[
    I4Image,
    I4AImage,
    I8Image,
    I8AImage,
    CI4Image,
    CI8Image,
    RGBAImage,
    RGBA5551Image,
]