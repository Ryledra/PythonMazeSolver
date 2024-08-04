from geometry import Cell, Point
from window import Window
from time import sleep
import random

class Maze:
    def __init__(self, top_corner: Point, num_rows: int, num_columns: int, 
    cell_size_x: int, cell_size_y: int, window: Window, seed=None):
        if seed is not None: random.seed(seed)
        self.top_corner: Point = top_corner
        self.num_rows, self.num_columns = num_rows, num_columns
        self.cell_size_x, self.cell_size_y = cell_size_x, cell_size_y
        self.window = window
        self._cells: list(list(Cell)) = []
        self._create_cells()
        self._break_entrance_exit()
        self._break_walls_r(0, 0)
        self._draw_maze()
        self._reset_cells_visited()

    def _create_cells(self):
        for y in range(self.num_rows):
            row = []
            for x in range(self.num_columns):
                row.append(
                    Cell(
                        self.window, 
                        Point(
                            self.top_corner.x + x * self.cell_size_x,
                            self.top_corner.y + y * self.cell_size_y
                        ), Point(
                            self.top_corner.x + (x+1) * self.cell_size_x,
                            self.top_corner.y + (y+1) * self.cell_size_y
                        )
                    )
                )
            #print(row)
            self._cells.append(row)

    def __repr__(self) -> str:
        formatted_cells = []
        for row in self._cells:
            for cell in row: formatted_cells.append(str(cell))
        return f"***** Maze: {self.num_rows}x{self.num_columns} *****\n{"\n".join(formatted_cells)}"

    def _draw_maze(self):
        #print(self)
        for row in self._cells:
            for cell in row:
                cell.draw()

    def _animate(self):
        self.window.redraw()
        sleep(0.05)

    def _break_entrance_exit(self):
        self.start_column = random.randint(0, self.num_columns - 1)
        self._cells[0][self.start_column].walls["top"] = False
        self.end_column = random.randint(0, self.num_columns - 1)
        self._cells[self.num_rows-1][self.end_column].walls["bottom"] = False

    def _get_valid_break_directions(self, row:int, column: int) -> list[list[int, int]]:
        ret: list[list[int, int]] = []
        if row > 0 and not self._cells[row-1][column].visited: 
            ret.append([row-1, column])
        if row < self.num_rows-1 and not self._cells[row+1][column].visited: 
            ret.append([row+1, column])
        if column > 0 and not self._cells[row][column-1].visited: 
            ret.append([row, column-1])
        if column < self.num_columns-1 and not self._cells[row][column+1].visited: 
            ret.append([row, column+1])
        return ret

    def _break_walls_r(self, row: int, column:int): #current = [row, col]
        self._cells[row][column].visited = True
        while True:
            valid_directions = list(self._get_valid_break_directions(row, column))
            if len(valid_directions) == 0: return
            r: int = random.randint(0, len(valid_directions) - 1)
            x, y = valid_directions.pop(r)
            # print(f"moving from {row, column} to {x, y}")
            if row > x:
                # print("\t moving up")
                self._cells[row][column].walls["top"] = False
                self._cells[ x ][ y ].walls["bottom"] = False
                # print('\t', self._cells[row][column].walls, self._cells[ x ][ y ].walls)
            elif row < x:
                # print("\t moving down")
                self._cells[row][column].walls["bottom"] = False
                self._cells[ x ][ y ].walls["top"] = False
                # print('\t', self._cells[row][column].walls, self._cells[ x ][ y ].walls)
            elif column > y:
                # print("\t moving left")
                self._cells[row][column].walls["left"] = False
                self._cells[ x ][ y ].walls["right"] = False
                # print('\t', self._cells[row][column].walls, self._cells[ x ][ y ].walls)
            elif column < y:
                # print("\t moving right")
                self._cells[row][column].walls["right"] = False
                self._cells[ x ][ y ].walls["left"] = False
                # print('\t', self._cells[row][column].walls, self._cells[ x ][ y ].walls)
            self._break_walls_r(x, y)

    def _reset_cells_visited (self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        print("starting to solve...")
        if self._solve_r(0, self.start_column):
            print("maze solved")
        else: print("No solution found")

    def _get_valid_move_directions(self, row: int, column:int) -> list[list[int, int]]:
        ret: list[list[int, int]] = []
        walls: dict[str, bool] = self._cells[row][column].walls
        if( not walls["bottom"] 
            and row < self.num_rows-1 
            and not self._cells[row+1][column].visited
        ): 
            ret.append([row+1, column])
        if( not walls["top"] 
            and row > 0
            and not self._cells[row-1][column].visited
        ): 
            ret.append([row-1, column])
        if( not walls["right"] 
            and column < self.num_columns-1 
            and not self._cells[row][column+1].visited
        ): 
            ret.append([row, column+1])
        if( not walls["left"] 
            and column > 0 
            and not self._cells[row][column-1].visited
        ): 
            ret.append([row, column-1])
        return ret

    def _solve_r(self, row: int, column: int) -> bool:
        self._animate()
        if row == self.num_rows - 1 and column == self.end_column:
            return True
        currentCell: Cell = self._cells[row][column]
        currentCell.visited = True
        valid_directions: list[list[int, int]] = self._get_valid_move_directions(row, column)
        # print(f"at cell ({row, column})", valid_directions)
        #if len(valid_directions) == 0: return False
        for direction in valid_directions:
            # print(f"\ttrying to move to ({direction[0], direction[1]})")
            currentCell.draw_move(self._cells[direction[0]][direction[1]])
            if self._solve_r(direction[0], direction[1]):
                return True
            currentCell.draw_move(self._cells[direction[0]][direction[1]], True)
        # print(f"\tno valid moves")
        return False