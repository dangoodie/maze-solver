from cell import Cell
from graphics import Window

def main():
    win  = Window(800, 600)
    
    c = Cell(win)
    c.draw(100,100,200,200)

    win.wait_for_close()

if __name__ == "__main__":
    main()
