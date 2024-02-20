# N64Tex-Python

An image converter for N64 image formats written in Python

## Description

This library is a Python implementation of 
[Isotarge's N64Tex Tool](https://github.com/Isotarge/n64tex)

The goal is to have an OS-agnostic tool for converting between N64 image formats, fill in the
missing CI image formats, and have a Python-importable library to function with my
[DK64-Lib Project](https://github.com/ThomasJRyan/dk64_lib)

## Installation

This package can be installed from PyPi using `pip`
```bash
pip install --upgrade n64tex
```

## Usage

The package can be used in one of two ways. Either with the bundle CLI tool, or through
a Python script itself.

### CLI

#### From Image

Convert from an RGBA image to RGBA5551
```bash
n64tex rgba_image.png rgba5551 -o rgba5551_image.png
# Produces rgba5551_image.png
```

Optionally, you can also write a raw bytes file
```bash
n64tex rgba_image.png rgba5551 -o rgba5551_image.png --write_bytes
# Produces rgba5551_image.png and rgba5551_image
```

Converting to a CI format will provide an accompanying palette file

#### From bytes

You can also give a byte-like file to convert to an image, but the format must be specified

Converting from RGBA5551 to RGBA
```bash
n64tex rgba5551_bytes rgba5551 rgba -o rgba_image.png
# Produces rgba_image.png
```

Converting from CI bytes requires a bytes-like palette to be provided
```bash
n64tex ci8_bytes ci8 rgba -o rgba_image.png --palette palette_ci8_bytes
```

### Python

Open an image and convert it to other formats
```python
from PIL import Image
from n64tex.formats import RGBAImage

image = Image.open('rgba_image.png')
rgba_image = RGBAImage.from_image(image)

rgba5551_image = rgba_image.to_rgba5551()
i8a_image = rgba_image.to_i8a()
ci8_image = rgba_image.to_ci8()

# Any of these objects can be saves to an image file using the .save() method
rgba5551_image.save('rgba5551_image.png')
i8a_image.save('i8a_image.png')
ci8_image.save('ci8_image.png')
```

Open a bytes-like image and convert it to other formats or save it as an image file
```python
from n64tex.formats import RGBA5551Image, CI8Image

with open('rgba5551_bytes', 'rb') as fil:
    rgba5551_image = RGBA5551Image.from_bytes(fil.read(), width=32, height=32)
rgba5551_image.save('rgba5551_image.png')

# CI file formats require a palette
with open('ci8_bytes', 'rb') as fil, open('palette_ci8_bytes', 'rb') as palette_fil:
    ci8_image = CI8Image.from_bytes(fil.read(), width=32, height=32, palette_bytes=palette_fil.read())
ci8_image.save('ci8_image.png')
```

