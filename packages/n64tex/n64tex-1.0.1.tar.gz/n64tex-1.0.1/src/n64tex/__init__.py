def cli() -> None:
    """Command line util"""
    import pathlib
    import argparse
    
    from PIL import Image, UnidentifiedImageError
    
    from n64tex.formats import Formats

    parser = argparse.ArgumentParser()

    parser.add_argument("filepath", help="Path to file to convert")
    
    parser.add_argument("--width", type=int, help="Width of image. Defaults to 64", default=64)
    parser.add_argument("--height", type=int, help="Height of image. Defaults to 64", default=64)

    parser.add_argument(
        "input_format",
        help="Input image format",
        type=str,
        choices=[
            "i4",
            "i4a",
            "i8",
            "i8a",
            "ci4",
            "ci8",
            "rgba",
            "rgba5551",
        ],
        nargs='?',
        default='rgba'
    )
    parser.add_argument(
        "output_format",
        help="Output image format",
        type=str,
        choices=[
            "i4",
            "i4a",
            "i8",
            "i8a",
            "ci4",
            "ci8",
            "rgba",
            "rgba5551",
        ],
    )
    
    parser.add_argument("--palette", help="File containing palette information. Only required for CI4/CI8 input format")

    parser.add_argument("--output_file", "-o", help="Output file name", type=str)
    parser.add_argument("--write_bytes", "-b", action="store_true", help="Write a bytes file")

    args = parser.parse_args()

    # Input filepath
    filepath = pathlib.Path(args.filepath)
    
    # Input and output formats
    input_format = args.input_format
    output_format = args.output_format
    
    # Output filepath
    output_file = filepath.parent / f'{output_format}_{filepath.name}'
    if args.output_file:
        output_file = pathlib.Path(args.output_file)
        
    # Palette information
    palette_data = None
    if args.palette:
        palette_path = pathlib.Path(args.palette)
        with open(palette_path, 'rb') as fil:
            palette_image = fil.read()
        obj = Formats.rgba5551.value.from_bytes(palette_image, 16, 16)
        palette_data = obj.to_bytes()

    # Convert image
    cls = Formats[input_format].value
    try:
        image = Image.open(filepath)
        width = image.width or args.width
        height = image.height or args.height
        obj = cls.from_image(image, width, height)
    except UnidentifiedImageError:
        with open(filepath, 'rb') as fil:
            image = fil.read()
        width = args.width
        height = args.height
        obj = cls.from_bytes(image, width, height, palette_data)
    converted_obj = obj.convert_to(Formats[output_format].value)
        
    # Handle writing to bytes
    if args.write_bytes:
        with open(output_file.parent / output_file.stem, 'wb') as fil:
            fil.write(converted_obj.to_bytes())
        if converted_obj.palette is not None:
            palette_path = output_file.parent / f'palette_{output_file.name}'
            with open(palette_path.parent / palette_path.stem, 'wb') as fil:
                fil.write(converted_obj.palette.astype('>u2').tobytes())
    
    # Save image
    converted_obj.save(output_file)
        