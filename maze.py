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
        win: Window = None,
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
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

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
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
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
        if self._win is None:
            return

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
        if i < 0 or i >= self._num_cols or j < 0 or j >= self._num_rows:
            return

        self._cells[i][j].visited = True

        while True:
            to_visit = []

            # Check neighbors and ensure indices are within bounds
            # Above (same column, row decreases)
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            # Below (same column, row increases)
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            # Left (column decreases, same row)
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            # Right (column increases, same row)
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))

            if not to_visit:
                # No more neighbors to visit, backtrack
                self._draw_cell(i, j)
                return

            # Pick a random neighbor
            r_cell = to_visit[random.randrange(len(to_visit))]

            # Break walls between current cell and the chosen neighbor
            self._remove_walls_between(i, j, r_cell[0], r_cell[1])

            # Recurse into the chosen neighbor
            self._break_walls_r(r_cell[0], r_cell[1])

    def _remove_walls_between(self, i, j, ni, nj):
        # knock out walls between this cell and the next cell(s)
        # right
        if ni == i + 1:
            self._cells[i][j].has_right_wall = False
            self._cells[ni][nj].has_left_wall = False
        # left
        if ni == i - 1:
            self._cells[i][j].has_left_wall = False
            self._cells[ni][nj].has_right_wall = False
        # down
        if nj == j + 1:
            self._cells[i][j].has_bottom_wall = False
            self._cells[ni][nj].has_top_wall = False
        # up
        if nj == j - 1:
            self._cells[i][j].has_top_wall = False
            self._cells[ni][nj].has_bottom_wall = False

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # above
        if (j > 0
                and not self._cells[i][j].has_top_wall
                and not self._cells[i][j - 1].visited
                ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # below
        if (j < self._num_rows - 1
                and not self._cells[i][j].has_bottom_wall
                and not self._cells[i][j + 1].visited
            ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        # left
        if (i > 0
                and not self._cells[i][j].has_left_wall
                and not self._cells[i - 1][j].visited
                ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # right
        if (i < self._num_cols - 1
                and not self._cells[i][j].has_right_wall
                and not self._cells[i + 1][j].visited
                ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        return False
