from tkinter import Tk, BOTH, Canvas
from geometry import Line

class Window:
    def __init__(self, width: int, height: int):
        self.tk: Tk = Tk()
        self.tk.title: str = "Maze Solver"
        self.canvas: Canvas = Canvas(self.tk, bg="white", height=height, width=width)
        self.canvas.pack()
        self.is_window_running: bool = False
        self.tk.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.tk.update_idletasks()
        self.tk.update()

    def wait_for_close(self):
        self.is_window_running = True
        while self.is_window_running:
            self.redraw()

    def close(self):
        self.is_window_running = False
 
    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)