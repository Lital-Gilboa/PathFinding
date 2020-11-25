import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # window
pygame.display.set_caption("Path Finding Algorithms Visualization")

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

# calculate the absolute distance between point 1 and point 2
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    # when current is start we done, start is not in came_from
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def A_star_algorithm(draw, grid, start, end):  # draw supposed to be a function
    count = 0
    current = start
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # store the: f score, count and the spot(node)
    came_from = {}  # dict
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())  # estimated the distance from start point to end point

    open_set_hash = {start}  # help to check if spot is in the open set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # get the spot, the first current is the start node
        open_set_hash.remove(current)

        if current == end:
            # make path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def BFS_algorithm(draw, grid, start, end):  # draw supposed to be a function
    count = 0
    current = start
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # store the: weight, count and the spot(node)
    came_from = {}  # dict
    weight = {spot: float("inf") for row in grid for spot in row}
    weight[start] = 0

    open_set_hash = {start}  # help to check if spot is in the open set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # get the spot, the first current is the start node
        open_set_hash.remove(current)

        if current == end:
            # make path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_weight = weight[current] + 1

            if temp_weight < weight[neighbor]:
                came_from[neighbor] = current
                weight[neighbor] = temp_weight
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((weight[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False



def algorithm(draw, grid, start, end, algorithm):  # draw supposed to be a function
    if(algorithm == A_star_algorithm):
        A_star_algorithm(draw, grid, start, end)
    elif(algorithm == BFS_algorithm):
        BFS_algorithm(draw, grid, start, end)


def make_grid(rows, width):
    grid = []
    gap = width // rows  # floor division
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows  # floor division
    # for every row draw horizontal line
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # for every row draw vertical line
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    # fill the screen
    win.fill(WHITE)

    # draw all the colors
    for row in grid:
        for spot in row:
            spot.draw(win)

    # draw the grid lines on top
    draw_grid(win, rows, width)

    # take what we just draw and display this
    pygame.display.update()


# translate the mouse position to the correct cube
def get_clicked_pos(pos, rows, width):
    gap = width // rows  # floor division
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# main loop
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    # initialize the start and end position
    start = None
    end = None

    # True if we run the main loop
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # the left key on the mouse is pressed
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()  # the mouse position on the screen
                row, col = get_clicked_pos(pos, ROWS, width)
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
                row, col = get_clicked_pos(pos, ROWS, width)  # translate to the right cube
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

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, BFS_algorithm)

                # clear the screen
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)









