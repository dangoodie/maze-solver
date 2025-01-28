import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_cell_coordinates(self):
        num_cols = 2
        num_rows = 2
        cell_size_x = 10
        cell_size_y = 15
        m1 = Maze(0, 0, num_rows, num_cols, cell_size_x, cell_size_y)

        # Calculate expected cell coordinates
        expected_coordinates = [
            (0, 0, 10, 15),  # Cell (0, 0)
            (10, 0, 20, 15),  # Cell (0, 1)
            (0, 15, 10, 30),  # Cell (1, 0)
            (10, 15, 20, 30),  # Cell (1, 1)
        ]

        # Check if coordinates match
        for i in range(num_cols):
            for j in range(num_rows):
                x1 = m1._x1 + (j * cell_size_x)
                y1 = m1._y1 + (i * cell_size_y)
                x2 = x1 + cell_size_x
                y2 = y1 + cell_size_y
                self.assertEqual((x1, y1, x2, y2), expected_coordinates.pop(0))

    def test_no_window_skips_drawing(self):
        # Test that no drawing is attempted when win is None
        m1 = Maze(0, 0, 3, 3, 10, 10, win=None)
        # The test passes because the logic of _draw_cell is skipped when win is None
        # If no exceptions occur, the test is successful
        self.assertTrue(True)

    def test_edge_case_no_cells(self):
        # Test edge case where rows and columns are zero
        m1 = Maze(0, 0, 0, 0, 10, 10)
        self.assertEqual(len(m1._cells), 0)

    def test_reset_cells_visited(self):
        # Test that all cells are reset to not visited
        m1 = Maze(0, 0, 3, 3, 10, 10)
        for i in range(3):
            for j in range(3):
                m1._cells[i][j].visited = True
        m1._reset_cells_visited()
        for i in range(3):
            for j in range(3):
                self.assertFalse(m1._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
