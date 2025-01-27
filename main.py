from maze import Maze
from graphics import Window

def main():
    win  = Window(800, 600)
    m = Maze(50, 50, 14, 10, 50, 50, win)
    win.wait_for_close()

if __name__ == "__main__":
    main()
