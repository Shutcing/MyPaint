from main import Canvas, app, pixels_to_dots
import tkinter as tk
from PIL import Image
import unittest


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(10, "black", "white")
        self.canvas.pen_weight = 10

    def test_canvas_initialization(self):
        self.assertEqual(self.canvas.pen_weight, 10)
        self.assertEqual(self.canvas.pen_color, "black")
        self.assertEqual(self.canvas.bg_color, "white")
        self.assertIsInstance(self.canvas.canvas, tk.Canvas)

    def test_canvas_show(self):
        self.canvas.show()
        self.assertEqual(self.canvas.canvas.cget("background"), "white")
        self.assertEqual(
            self.canvas.canvas.cget("width"), "1200"
        )
        self.assertEqual(
            self.canvas.canvas.cget("height"), "800"
        )

    def test_canvas_Draw(self):
        event = type("", (), {})()
        event.x = 0
        event.y = 0
        app.app.configure(cursor="@paint_img/pen.cur")
        for _ in range(10):
            event.x += 10
            event.y += 10
            self.canvas.draw(event)
        self.assertEqual(len(self.canvas.canvas.find_withtag("line")), 9)
        app.app.configure(cursor="@paint_img/eraser.cur")
        for _ in range(10):
            event.x -= 10
            event.y -= 10
            self.canvas.draw(event)
        self.assertEqual(len(self.canvas.canvas.find_withtag("eraser")), 10)

    def test_stop_draw_creates_rectangle(self):
        for figure in ["square", "circle", "triangle", "line"]:
            app.app.configure(cursor=f"@paint_img/{figure}.cur")
            event = type("", (), {})()
            event.x, event.y = 0, 0
            for _ in range(10):
                event.x += 10
                event.y += 10
                self.canvas.draw(event)
            self.canvas.stop_draw(event)
            self.assertEqual(len(self.canvas.canvas.find_withtag("final_figure")), 1)
            self.assertEqual(len(self.canvas.canvas.find_withtag("figure")), 0)
            self.canvas.canvas.delete("all")

    def test_pixel_to_dots(self):
        pixels = [1, 100, 0]
        dots = [96 / 72, (96 / 72) * 100, 0]
        for i in range(len(pixels)):
            self.assertEqual(pixels_to_dots(pixels[i]), dots[i])

    def test_key_press(self):
        self.canvas.text_id = self.canvas.canvas.create_text(0, 0, text="", font=("Montserat", 50), fill="black")
        event = type("", (), {})()
        event.char = "E"
        event.keysym = ""
        self.canvas.key_press(event)
        self.assertEqual(self.canvas.canvas.itemcget(self.canvas.text_id, "text"), "E")


    def test_merge_images(self):
        image1 = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        image2 = Image.new('RGBA', (100, 100), (155, 0, 0, 155))
        
        expected_image = Image.new('RGBA', (100, 100), (194, 0, 0, 194))
        expected_image.paste(image1, (0, 0))
        expected_image.paste(image2, (0, 0), image2)
        
        result_image = self.canvas.merge_images(image1, image2)
        
        self.assertEqual(result_image.getpixel((50, 50)), expected_image.getpixel((50, 50)))

    
    def test_save(self):
        self.canvas.save("red")
        img = Image.open("myimage.png")
        color = img.getpixel((50, 50))
        self.assertEqual(color, (155, 155, 155, 0))




if __name__ == "__main__":
    unittest.main()
