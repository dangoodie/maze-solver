from maze import Maze
from graphics import Window

def main():
    win  = Window(800, 600)
    m = Maze(0, 0, 16, 12, 50, 50, win)
    win.wait_for_close()

if __name__ == "__main__":
    main()
