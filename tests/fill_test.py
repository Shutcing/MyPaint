import unittest
import tkinter as tk
from PIL import Image
from fill import fill


class TestFillFunction(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=10, height=10)
        self.canvas.pack()

    def tearDown(self):
        self.root.destroy()

    def create_image(self, size, color):
        image = Image.new("RGBA", size, color)
        return image

    def test_fill_on_empty_image(self):
        image = self.create_image((10, 10), (0, 0, 0, 0))
        fill(self.canvas, image, 5, 5, 'red')
        rectangles = self.canvas.find_all()
        self.assertEqual(len(rectangles), 100)

    def test_fill_on_non_transparent_image(self):
        image = self.create_image((10, 10), (255, 255, 255, 255))
        fill(self.canvas, image, 5, 5, 'red')
        rectangles = self.canvas.find_all()
        self.assertEqual(len(rectangles), 0)

    def test_fill_partial_transparency(self):
        image = self.create_image((10, 10), (255, 255, 255, 0))
        pixels = image.load()
        pixels[5, 5] = (255, 255, 255, 255)
        fill(self.canvas, image, 4, 4, 'red')
        rectangles = self.canvas.find_all()
        self.assertEqual(len(rectangles), 99)

    def test_fill_edge_case(self):
        image = self.create_image((10, 10), (255, 255, 255, 0))
        fill(self.canvas, image, 0, 0, 'red')
        rectangles = self.canvas.find_all()
        self.assertEqual(len(rectangles), 100)

if __name__ == '__main__':
    unittest.main()