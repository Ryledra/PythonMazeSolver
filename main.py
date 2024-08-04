from geometry import Point
from window import Window
from maze import Maze

def Solve(maze: Maze):
    maze.solve()

def main():
    window: Window = Window(820, 620)
    maze: Maze = Maze(
            Point(10,10),
            30, 40,
            20, 20,
            window
        )
    Solve(maze)
    window.wait_for_close()

if __name__ == "__main__":
    main()
