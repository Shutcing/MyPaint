import unittest
from filters import find_rectangles_intersection, bright, hex_to_rgb, rgb_to_hex, convert_to_black_or_white, filt_img
from PIL import Image

class TestFilters(unittest.TestCase):

    def test_P(self):
        point1 = (1, 1)
        point2 = (3, 3)
        point3 = (2, 2)
        point4 = (4, 4)
        result = find_rectangles_intersection(point1, point2, point3, point4)
        self.assertEqual(result, [0, 0, 1, 1])

    def test_bright(self):
        self.assertEqual(bright("#000000", 1), "#000000")
        self.assertEqual(bright("#ffffff", 0.5), "#7f7f7f")
        self.assertEqual(bright("#ff0000", 2), "#ff0000")
        with self.assertRaises(ValueError):
            bright("#ff0000", 3)

    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#ff0000"), (255, 0, 0))

    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex((0, 0, 0)), "#000000")
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")
        self.assertEqual(rgb_to_hex((255, 0, 0)), "#ff0000")
        with self.assertRaises(ValueError):
            rgb_to_hex((256, 0, 0))
        with self.assertRaises(ValueError):
            rgb_to_hex((0, -1, 0))

    def test_convert_to_black_or_white(self):
        self.assertEqual(convert_to_black_or_white("black"), "#000000")
        self.assertEqual(convert_to_black_or_white("#ff0000"), "#555555")
        self.assertEqual(convert_to_black_or_white("#00ff00"), "#555555")
        self.assertEqual(convert_to_black_or_white("#0000ff"), "#555555")

    def test_filt_img(self):
        img = Image.new("RGBA", (10, 10), "white")
        area = [0, 0, 5, 5]
        bright_index = 1.5
        filter_name = "brighten"
        canvas = MockCanvas()
        result_img = filt_img(img, area, bright_index, filter_name, canvas)
        for x in range(5):
            for y in range(5):
                r, g, b, a = result_img.getpixel((x, y))
                self.assertEqual((r, g, b), (255, 255, 255))

class MockCanvas:
    def __init__(self):
        self.choose_select_place = [(0, 0), (5, 5)]
        self.canvas = self
        self.img_to_insert = []

    def bbox(self, tag):
        return (0, 0, 10, 10)

    def find_withtag(self, tag):
        return [1]

    def Change_img(self, tag, file):
        pass

if __name__ == "__main__":
    unittest.main()
