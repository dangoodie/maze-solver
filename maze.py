import time
import random

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win=None,
            seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed is not None:
            self._seed = random.seed(seed)
        else:
            self._seed = random.seed()

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + (j * self._cell_size_x)
        y1 = self._y1 + (i * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # top left
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._animate()

        # bottom right
        i = self._num_cols - 1
        j = self._num_rows - 1
        self._cells[i][j].has_bottom_wall = False
        self._draw_cell(i, j)
        self._animate()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []

            # Check neighbors and ensure indices are within bounds
            if j > 0 and not self._cells[i][j - 1].visited:  # Above
                to_visit.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:  # Below
                to_visit.append((i, j + 1))
            if i > 0 and not self._cells[i - 1][j].visited:  # Left
                to_visit.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:  # Right
                to_visit.append((i + 1, j))

            if not to_visit:
                # No more neighbors to visit, backtrack
                self._draw_cell(i, j)
                return

            # Pick a random neighbor
            r_cell = to_visit[random.randint(0, len(to_visit) - 1)]

            # Break walls between current cell and the chosen neighbor
            if i == r_cell[0]:  # Same row
                if j < r_cell[1]:  # Neighbor is below
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[r_cell[0]][r_cell[1]].has_top_wall = False
                else:  # Neighbor is above
                    self._cells[i][j].has_top_wall = False
                    self._cells[r_cell[0]][r_cell[1]].has_bottom_wall = False
            else:  # Same column
                if i < r_cell[0]:  # Neighbor is to the right
                    self._cells[i][j].has_right_wall = False
                    self._cells[r_cell[0]][r_cell[1]].has_left_wall = False
                else:  # Neighbor is to the left
                    self._cells[i][j].has_left_wall = False
                    self._cells[r_cell[0]][r_cell[1]].has_right_wall = False

            # Recurse into the chosen neighbor
            self._break_walls_r(r_cell[0], r_cell[1])
