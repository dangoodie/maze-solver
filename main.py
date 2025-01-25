from graphics import *

def main():
    win  = Window(800, 600)

    win.draw_line(Line(Point(100,100), Point(400,400)), "red")
    win.draw_line(Line(Point(400,100), Point(100,400)), "red")

    win.wait_for_close()

if __name__ == "__main__":
    main()
