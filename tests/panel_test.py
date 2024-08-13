import unittest
import customtkinter as ctk
from panel import Panel


class TestPanel(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.panel = Panel(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertIsInstance(self.panel.frame, ctk.CTkFrame)
        self.assertEqual(self.panel.buttons, [])
        self.assertEqual(self.panel.figure_bar, [])
        self.assertEqual(self.panel.width, 0)
        self.assertEqual(self.panel.height, 0)
        self.assertEqual(self.panel.x, 0)
        self.assertEqual(self.panel.y, 0)
        self.assertEqual(self.panel.color, "")
        self.assertEqual(self.panel.label, "")

    def test_hide(self):
        self.panel.hide()
        self.assertFalse(
            self.panel.frame.winfo_ismapped()
        )

    def test_show(self):
        self.panel.show(
            width=200,
            height=100,
            color="red",
            bg_color="white",
            x=50,
            y=50,
            corner_r=10,
        )
        self.assertEqual(self.panel.width, 200)
        self.assertEqual(self.panel.height, 100)
        self.assertEqual(self.panel.color, "red")
        self.assertEqual(self.panel.x, 50)
        self.assertEqual(self.panel.y, 50)

        self.assertEqual(self.panel.frame.cget("width"), 200)
        self.assertEqual(self.panel.frame.cget("height"), 100)
        self.assertEqual(self.panel.frame.cget("fg_color"), "red")
        self.assertEqual(self.panel.frame.cget("bg_color"), "white")
        self.assertEqual(self.panel.frame.cget("corner_radius"), 10)


if __name__ == "__main__":
    unittest.main()
