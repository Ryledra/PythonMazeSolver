from geometry import Point
from window import Window
from maze import Maze

def Solve(maze: Maze):
    maze.solve()

def main():
    window: Window = Window(800, 600)
    maze: Maze = Maze(
            Point(10,10),
            11, 15,
            50, 50,
            window
           )
    Solve(maze)
    window.wait_for_close()

if __name__ == "__main__":
    main()
