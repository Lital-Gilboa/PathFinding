import pygame
import Algorithms
import argparse

# any color have a meaning - start point, end point etc.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# this class represent all the nodes and their characteristics : color, size, location etc.
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # keep track the current position of this spot on the screen
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.is_markes = False

    # indexing spot using row and col
    def get_pos(self):
        return self.row, self.col

    # check if we already visited this spot
    def is_closed(self):
        return self.color == RED

    # check if this spot is in the open set
    def is_open(self):
        return self.color == GREEN

    # check if this spot is a obstacle
    def is_barrier(self):
        return self.color == BLACK

    # check if this spot is the start point
    def is_start(self):
        return self.color == ORANGE

    # check if this spot is the end point
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    # draw this spot on the screen (win)
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        # UP neighbor
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT neighbor
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # DOWN neighbor
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # LEFT neighbor
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # compare this spot to the other spot (for the PriorityQueue)
    def __lt__(self, other):
        return False;

class PathFinder():

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-algorithm_name", default='A_star', choices=['A_star', 'DFS', 'BFS', 'Dijkstra'],  help="please choose a algorithm : A_star, BFS, DFS, Dijkstra")
        parser.add_argument("-rows", default=50, type=int, help="")
        parser.add_argument("-width", default=800, type=int, help="")
        self.args = parser.parse_args()
        self.win = pygame.display.set_mode((self.args.width, self.args.width))  # window
        pygame.display.set_caption("Path Finding Algorithms Visualization")

    def run_algorithm(self, algorithm):  # draw supposed to be a function
        algorithm.execute_callback(algorithm.name)

    def make_grid(self):
        grid = []
        gap = self.args.width // self.args.rows  # floor division
        for i in range(self.args.rows):
            grid.append([])
            for j in range(self.args.rows):
                spot = Spot(i, j, gap, self.args.rows)
                grid[i].append(spot)
        return grid

    def draw_grid(self):
        gap = self.args.width // self.args.rows  # floor division
        # for every row draw horizontal line
        for i in range(self.args.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.args.width, i * gap))
            # for every row draw vertical line
            for j in range(self.args.rows):
                pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.args.width))

    def draw(self, grid):
        # fill the screen
        self.win.fill(WHITE)
        # draw all the colors
        for row in grid:
            for spot in row:
                spot.draw(self.win)
        # draw the grid lines on top
        self.draw_grid()
        # take what we just draw and display this
        pygame.display.update()

    # translate the mouse position to the correct cube
    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows  # floor division
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

    # main loop
    def main(self):
        grid = self.make_grid()
        # initialize the start and end position
        start = None
        end = None
        # True if we run the main loop
        run = True
        while run:
            self.draw(grid)
            for event in pygame.event.get():
                if run == False:
                    break
                if event.type == pygame.QUIT:
                    run = False

                # the left key on the mouse is pressed
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()  # the mouse position on the screen
                    row, col = self.get_clicked_pos(pos, self.args.rows, self.args.width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    # we already defined the start and end positions
                    elif start and end and spot != start and spot != end:
                        spot.make_barrier()
                # the right key on the mouse is pressed
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()  # the mouse position on the screen
                    row, col = self.get_clicked_pos(pos, self.args.rows, self.args.width)  # translate to the right cube
                    spot = grid[row][col]
                    spot.reset()
                    # the two variables that were initialized
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                # the key is pressed down
                if event.type == pygame.KEYDOWN:
                    # the key is the space key
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        algorithm = Algorithms.Algorithm(self.win, lambda: self.draw(grid), grid, start, end, self.args.algorithm_name)
                        try:
                            self.run_algorithm(algorithm)
                        except pygame.error:
                            run = False
                            continue
                    # clear the screen
                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = self.make_grid()
        pygame.quit()


if __name__ == '__main__':
    path_finder_obj = PathFinder()
    path_finder_obj.main()







