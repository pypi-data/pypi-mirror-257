import unittest

import numpy as np

from n64tex.formats import (
    RGBAImage,
    RGBA5551Image,
    I4Image,
    I8Image,
    I4AImage,
    I8AImage,
    CI4Image,
    CI8Image,
)


class TestRGBAImage(unittest.TestCase):
    def setUp(self) -> None:
        self.image = RGBAImage.from_bytes(
            raw_bytes=b"\xff\x00\x00\xff\x00\xff\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array(
                    [
                        [[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255]],
                        [[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 0]],
                    ],
                    dtype=np.uint8,
                )
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\xff\x00\x00\xff\x00\xff\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00",
        )

    def test_conversion_to_rgba5551(self):
        self.assertTrue(
            (
                self.image.to_rgba5551().data_array
                == np.array([[63489, 1985, 63], [1, 65535, 65534]], dtype=np.uint16)
            ).all()
        )

    def test_conversion_to_i4(self):
        self.assertTrue(
            (
                self.image.to_i4().data_array
                == np.array([[8, 8, 8], [4, 15, 11]], dtype=np.uint8)
            ).all()
        )

    def test_conversion_to_i8(self):
        self.assertTrue(
            (
                self.image.to_i8().data_array
                == np.array([[127, 127, 127], [63, 255, 191]], dtype=np.uint8)
            ).all()
        )

    def test_conversion_to_i4a(self):
        self.assertTrue(
            (
                self.image.to_i4a().data_array
                == np.array([[8, 8, 8], [4, 15, 11]], dtype=np.uint8)
            ).all()
        )

    def test_conversion_to_ci4(self):
        self.assertTrue(
            (
                self.image.to_ci4().data_array
                == np.array([[3, 2, 1], [0, 5, 4]], dtype=np.uint8)
            ).all()
        )

    def test_conversion_to_ci4_palette(self):
        self.assertTrue(
            (
                self.image.to_ci4().palette
                == np.array([1, 63, 1985, 63489, 65534, 65535], dtype=np.uint16)
            ).all()
        )

    def test_conversion_to_ci8(self):
        self.assertTrue(
            (
                self.image.to_ci8().data_array
                == np.array([[3, 2, 1], [0, 5, 4]], dtype=np.uint8)
            ).all()
        )

    def test_conversion_to_ci8_palette(self):
        self.assertTrue(
            (
                self.image.to_ci8().palette
                == np.array([1, 63, 1985, 63489, 65534, 65535], dtype=np.uint16)
            ).all()
        )

class TestRGBA5551Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = RGBA5551Image.from_bytes(
            raw_bytes=b"\xf8\x01\x07\xc1\x00?\x00\x01\xff\xff\xff\xfe",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[63489, 1985, 63], [1, 65535, 65534]], dtype=np.uint16)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\xf8\x01\x07\xc1\x00?\x00\x01\xff\xff\xff\xfe",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [[248, 0, 0, 255], [0, 248, 0, 255], [0, 0, 248, 255]],
                        [[0, 0, 0, 255], [248, 248, 248, 255], [248, 248, 248, 0]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestI4Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = I4Image.from_bytes(
            raw_bytes=b"\x77\x73\xFB",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[7, 7, 7], [3, 15, 11]], dtype=np.uint8)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x07\x07\x07\x03\x0f\x0b",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [119, 119, 119, 119],
                            [119, 119, 119, 119],
                            [119, 119, 119, 119],
                        ],
                        [[51, 51, 51, 51], [255, 255, 255, 255], [187, 187, 187, 187]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestI8Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = I8Image.from_bytes(
            raw_bytes=b"\x7f\x7f\x7f?\xff\xbf",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[127, 127, 127], [63, 255, 191]], dtype=np.uint8)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x7f\x7f\x7f?\xff\xbf",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [127, 127, 127, 127],
                            [127, 127, 127, 127],
                            [127, 127, 127, 127],
                        ],
                        [[63, 63, 63, 63], [255, 255, 255, 255], [191, 191, 191, 191]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestIA4Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = I4AImage.from_bytes(
            raw_bytes=b"\x77\x73\xFB",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[7, 7, 7], [3, 15, 11]], dtype=np.uint8)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x07\x07\x07\x03\x0f\x0b",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [109, 109, 109, 255],
                            [109, 109, 109, 255],
                            [109, 109, 109, 255],
                        ],
                        [[36, 36, 36, 255], [255, 255, 255, 255], [182, 182, 182, 255]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestIA8Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = I8AImage.from_bytes(
            raw_bytes=b"\x7f\x7f\x7f?\xff\xbf",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[127, 127, 127], [63, 255, 191]], dtype=np.uint8)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x7f\x7f\x7f?\xff\xbf",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [119, 119, 119, 255],
                            [119, 119, 119, 255],
                            [119, 119, 119, 255],
                        ],
                        [[51, 51, 51, 255], [255, 255, 255, 255], [187, 187, 187, 255]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestCI4Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = CI4Image.from_bytes(
            raw_bytes=b"\x32\x10\x54",
            width=3,
            height=2,
            palette_bytes=b"\x00\x01\x00?\x07\xc1\xf8\x01\xff\xfe\xff\xff",
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[3, 2, 1], [0, 5, 4]], dtype=np.uint8)
            ).all(),
        )

    def test_palette(self):
        self.assertTrue(
            (
                self.image.palette
                == np.array([1, 63, 1985, 63489, 65534, 65535], dtype=np.uint16)
            ).all()
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x03\x02\x01\x00\x05\x04",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [[248, 0, 0, 255], [0, 248, 0, 255], [0, 0, 248, 255]],
                            [[0, 0, 0, 255], [248, 248, 248, 255], [248, 248, 248, 0]],
                        ],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )
        
    def test_oversized_palette(self):
        self.assertRaises(AssertionError, CI4Image, None, None, None, np.arange(17))


class TestCI8Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = CI8Image.from_bytes(
            raw_bytes=b'\x03\x02\x01\x00\x05\x04',
            width=3,
            height=2,
            palette_bytes=b"\x00\x01\x00?\x07\xc1\xf8\x01\xff\xfe\xff\xff",
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[3, 2, 1], [0, 5, 4]], dtype=np.uint8)
            ).all(),
        )

    def test_palette(self):
        self.assertTrue(
            (
                self.image.palette
                == np.array([1, 63, 1985, 63489, 65534, 65535], dtype=np.uint16)
            ).all()
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.to_bytes(),
            b"\x03\x02\x01\x00\x05\x04",
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [
                            [[248, 0, 0, 255], [0, 248, 0, 255], [0, 0, 248, 255]],
                            [[0, 0, 0, 255], [248, 248, 248, 255], [248, 248, 248, 0]],
                        ],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )
        
    def test_oversized_palette(self):
        self.assertRaises(AssertionError, CI8Image, None, None, None, np.arange(257))


if __name__ == "__main__":
    unittest.main()
