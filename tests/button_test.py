import unittest
from PIL import Image
from main import MyButton, Bar
from main import app, Panel


class TestMyButton(unittest.TestCase):
    def setUp(self):
        self.frame = Panel(app.app)
        self.my_button = MyButton(self.frame, "test_type")

    def test_button_initialization(self):
        self.assertEqual(self.my_button.type, "test_type")

    def test_button_show(self):
        self.my_button.show(
            50,
            50,
            "blue",
            "white",
            "Test",
            Image.open("paint_img/pen.png"),
            10,
            10,
            20,
            20,
            "test_type",
        )
        self.assertEqual(self.my_button.button.cget("text"), "Test")
        self.assertEqual(self.my_button.button.cget("fg_color"), "blue")

    def test_button_change_cursor(self):
        self.my_button.type = "pen"
        self.my_button.change_cursor()
        self.assertEqual(app.app.cget("cursor"), "@paint_img/pen.cur")

    def test_button_change_cursor_to_arrow(self):
        self.my_button.type = "figure"
        self.my_button.change_cursor()
        self.assertEqual(app.app.cget("cursor"), "arrow")

    def test_choose_tool(self):
        self.my_button.type = "pen"
        self.my_button.choose_tool()
        self.assertEqual(self.my_button.button.cget("fg_color"), "#67770A")

        self.my_button.type = "filtrs"
        self.my_button.frame = Panel(app.app)
        self.my_button.frame.figure_bar = Bar(self.my_button.frame.frame, [])
        self.my_button.choose_tool()
        self.assertEqual(app.bottom_panel.figure_bar.frame.cget("fg_color"), "#67770A")
        self.assertEqual(app.tools_panel.figure_bar.is_bar_show, False)

        self.my_button.type = "bright"
        self.my_button.choose_tool()
        self.assertEqual(app.bottom_panel.bright_level.frame.cget("fg_color"), "black")

        self.my_button.type = "plus"
        self.my_button.choose_tool()
        self.assertEqual(app.bottom_panel.bright_level.label.cget("text"), "1.1")

        self.my_button.type = "ok"
        app.canvas.choose_place = [(0, 0), (10, 10)]
        self.my_button.choose_tool()
        self.assertEqual(app.bottom_panel.bright_level.frame.winfo_exists(), 0)

    def test_change_buttons(self):
        MyButton.change_buttons(
            app.tools_panel,
            100,
            100,
            "black",
            "white",
            0,
            0,
            0,
            0,
            ["pen", "eraser", "figure", "size", "text"],
            100,
            100,
        )
        self.assertEqual(app.tools_panel.buttons[0].button.cget("fg_color"), "black")


if __name__ == "__main__":
    unittest.main()

