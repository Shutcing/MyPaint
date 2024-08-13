import unittest
import customtkinter as ctk
from weight_chooser import (
    WeightChooser,
)


class TestWeightChooser(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()
        self.weight_chooser = WeightChooser(
            self.frame, width=100, weight=10, color="red"
        )

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertEqual(self.weight_chooser.weight, 10)
        self.assertEqual(self.weight_chooser.scale_width, 100)
        self.assertEqual(self.weight_chooser.scale.cget("fg_color"), "red")
        self.assertEqual(self.weight_chooser.slider.cget("fg_color"), "red")

    def test_show(self):
        self.weight_chooser.show(50, 50, 15)
        self.assertEqual(self.weight_chooser.weight, 15)
        self.assertEqual(self.weight_chooser.scale_x, 50)
        self.assertEqual(self.weight_chooser.scale_y, 50)
        self.assertEqual(self.weight_chooser.slider_x, 50)
        self.assertEqual(self.weight_chooser.slider_y, 50 - 15 * 0.8)

    def test_hide(self):
        self.weight_chooser.hide()
        self.assertFalse(
            self.weight_chooser.scale.winfo_ismapped()
        )
        self.assertFalse(
            self.weight_chooser.slider.winfo_ismapped()
        )

    def test_update_slider(self):
        event = type("", (), {})()
        event.x = 0
        self.weight_chooser.show(
            50, 50, 10
        )
        initial_x = self.weight_chooser.slider_x
        for i in range(500):
            self.weight_chooser.update_slider(event)
            event.x += i
        new_x = self.weight_chooser.slider_x
        new_weight = self.weight_chooser.weight
        self.assertNotEqual(initial_x, new_x)
        self.assertGreater(new_weight, 10)


if __name__ == "__main__":
    unittest.main()