import unittest
from main import Bar, Panel, MyButton, app


class TestBar(unittest.TestCase):
    def setUp(self):
        self.figurebar_panel_buttons = ["option1", "option2", "option3"]
        self.bar = Bar(app.app, self.figurebar_panel_buttons)

    def test_init(self):
        self.assertIsInstance(self.bar, Panel)
        self.assertFalse(self.bar.is_bar_show)
        self.assertEqual(self.bar.options, self.figurebar_panel_buttons)

    def test_show(self):
        x, y = 10, 20
        width, height = 100, 50
        fg_color = "red"
        self.bar.show(x, y, width, height, fg_color, "black")

        self.assertTrue(self.bar.is_bar_show)

    def test_hide(self):
        self.bar.is_bar_show = True
        self.bar.hide()
        self.assertFalse(self.bar.is_bar_show)
        self.assertEqual(self.bar.is_bar_show, False)

    def test_destroy_buttons(self):
        button1 = MyButton(self.bar, "pen")
        button2 = MyButton(self.bar, "eraser")
        self.bar.buttons = [button1, button2]

        for i in self.bar.buttons:
            self.assertEqual(1, i.button.winfo_exists())
        self.bar.destroy_buttons()
        for i in self.bar.buttons:
            self.assertEqual(0, i.button.winfo_exists())


if __name__ == "__main__":
    unittest.main()