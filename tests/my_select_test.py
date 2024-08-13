import unittest
from my_select import (
    select,
    move_selection,
    choose_selection,
    cancel_selection,
    delete_selection,
    items,
)
from main import Canvas


class TestSelectionFunctions(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(10, "black", "white")
        self.canvas.show()
        self.canvas.choose_select_place = []

    def test_select(self):
        select(self.canvas, 50, 50, 150, 150, False)
        self.assertEqual(self.canvas.canvas.find_withtag("eraser_rect")[0] in self.canvas.canvas.find_overlapping(100, 100, 110, 110), True)

    def test_move_selection(self):
        global items
        select(self.canvas, 50, 50, 150, 150, False)
        id = self.canvas.canvas.create_rectangle(60, 60, 100, 100)
        items.append(id)
        initial_coords = self.canvas.canvas.coords(items[-1])

        mock_event = type("", (), {})()
        mock_event.x = 150
        mock_event.y = 150
        for _ in range(10):
            mock_event.x += 10
            mock_event.y += 10
            move_selection(mock_event)

        new_coords = self.canvas.canvas.coords(items[0])
        self.assertNotEqual(initial_coords, new_coords)
        self.assertEqual(
            self.canvas.choose_select_place,
            [(mock_event.x - 100, mock_event.y - 100), (mock_event.x, mock_event.y)],
        )

    def test_choose_selection(self):
        choose_selection(None)
        self.assertIn("<Button-1>", self.canvas.canvas.bind())

    def test_cancel_selection(self):
        select(self.canvas, 50, 50, 150, 150, False)
        self.canvas.canvas.create_rectangle(
            200, 200, 300, 300, fill="red", tags="selection"
        )
        items_before = list(items)
        cancel_selection(None)
        self.assertNotIn(items_before[0], self.canvas.canvas.find_withtag("selection"))
        self.assertIn("<Motion>", self.canvas.canvas.bind())

    def test_delete_selection(self):
        select(self.canvas, 50, 50, 150, 150, False)
        delete_selection(None)
        self.assertEqual(self.canvas.canvas.find_withtag("selection"), ())
        self.assertIn("<Motion>", self.canvas.canvas.bind())


if __name__ == "__main__":
    unittest.main()
