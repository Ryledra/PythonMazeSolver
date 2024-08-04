class Point:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def reorder(self, other):
        point_TL: Point = Point(min([self.x, other.x]), min([self.y, other.y]))
        point_BR: Point = Point(max([self.x, other.x]), max([self.y, other.y]))
        return point_TL, point_BR

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Point(x:{self.x}, y:{self.y})"


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.start: Point = point1
        self.end: Point = point2

    def draw(self, canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y,
            self.end.x, self.end.y,
            fill=fill_color, width=2
        )
    
    def __eq__(self, other) -> bool:
        return self.start == other.start and self.end == self.end

    def __repr__(self) -> str:
        return f"Line:(Start:{self.start}, End:{self.end}"

class Cell:
    def __init__(self, window, point1: Point, point2: Point, walls: dict[str, bool]=None):
        # walls = {left: T/F, right:T/F, top: T/F, bottom: T/f}
        if walls is None:
            walls = {
                    "left":  True,
                    "right": True,
                    "top":   True,
                    "bottom":True
                    }
        self.walls = walls
        p1: Point
        p2: Point
        p1, p2 = point1.reorder(point2)
        self.points: dict[str, Point] = {"t_l": p1, "b_r": p2}
        self.window = window
        self.visited: bool = False

    def __repr__(self) -> str:
        return f"Cell(Points({self.points['t_l']},{self.points['b_r']})\t{self.walls})"

    def draw(self):
        # print(f"drawing {self}")
        if self.window is None: return
        if self.walls["left"]:
            self.window.draw_line(
                Line(
                    self.points["t_l"], 
                    Point(self.points["t_l"].x, self.points["b_r"].y)
                ),
                "black"
            )
        if self.walls["right"]:
            self.window.draw_line(
                Line(
                    Point(self.points["b_r"].x, self.points["t_l"].y), 
                    self.points["b_r"]
                ),
                "black"
            )
        if self.walls["bottom"]:
            self.window.draw_line(
                Line(
                    Point(self.points["t_l"].x, self.points["b_r"].y),
                    self.points["b_r"]
                ),
                "black"
            )
        if self.walls["top"]:
            self.window.draw_line(
                Line(
                    self.points["t_l"],
                    Point(self.points["b_r"].x, self.points["t_l"].y)
                ),
                "black"
            )

    def get_centre(self) -> Point:
        return Point((self.points["t_l"].x + self.points["b_r"].x) // 2,
                     (self.points["t_l"].y + self.points["b_r"].y) // 2)

    def draw_move(self, to_cell, undo=False):
        colour: str = 'red'
        if undo: colour = 'gray'
        self.window.draw_line(
            Line(
                self.get_centre(), to_cell.get_centre()
            ),
            colour
        )
