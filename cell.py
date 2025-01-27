from graphics import *

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return

        # ensure smaller goes in x1 and y1
        if x1 < x2:
            self._x1 = x1
            self._x2 = x2
        else:
            self._x1 = x2
            self._x2 = x1

        if y1 < y2:
            self._y1 = y1
            self._y2 = y2
        else:
            self._y1 = y2
            self._y2 = y1

        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)))

    def draw_move(self, to_cell: "Cell", undo=False):
        fill_color = "red"
        if undo:
            fill_color = "gray"
        
        this_centre = self._find_centre_point()
        to_centre = to_cell._find_centre_point()
        print(this_centre)
        print(to_centre)
        print(fill_color)

        self._win.draw_line(Line(this_centre, to_centre), fill_color)

    def _find_centre_point(self) -> Point:
        x = abs((self._x2 - self._x1)) // 2 + self._x1 
        y = abs((self._y2 - self._y1)) // 2 + self._y1
        return Point(x, y)