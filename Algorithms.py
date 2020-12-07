import pygame
import math
from queue import PriorityQueue
import sys
from queue import Queue


class Algorithm():
    def __init__(self, win, draw, grid, start, end, name):  # draw supposed to be a function
        self.draw = draw
        self.grid = grid
        self.start = start
        self.end = end
        self.name = name
        self.ended = False
        self.win = win
        sys.setrecursionlimit(2500)


    def reconstruct_path(self, came_from, current):
        # when current is start we done, start is not in came_from
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw()

    def A_star(self):
        count = 0
        current = self.start
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))  # store the: f score, count and the spot(node)
        came_from = {}  # dict
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[self.start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[self.start] = h(self.start.get_pos(), self.end.get_pos())  # estimated the distance from start point to end point

        open_set_hash = {self.start}  # help to check if spot is in the open set

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]  # get the spot, the first current is the start node
            open_set_hash.remove(current)

            if current == self.end:
                # make path
                reconstruct_path(came_from, current, self.draw)
                self.end.make_end()
                self.start.make_start()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), self.end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            self.draw()

            if current != self.start:
                current.make_closed()

        return False

    def BFS(self):  # draw supposed to be a function
        current = self.start
        open_set = [] # Queue
        open_set.append(self.start)  # store the: weight, count and the spot(node)
        came_from = {}  # dict
        distance = {spot: float("inf") for row in self.grid for spot in row}
        distance[self.start] = 0

        while len(open_set) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.pop(0)  # get the spot, the first current is the start node

            if current == self.end:
                # make path
                reconstruct_path(came_from, self.end, self.draw)
                self.end.make_end()
                self.start.make_start()
                return True

            for neighbor in current.neighbors:
                if not neighbor.is_closed() and not neighbor.is_open() and not neighbor.is_start():
                    open_set.append(neighbor)
                    neighbor.make_open()
                    distance[neighbor] = distance[current] + 1
                    came_from[neighbor] = current
                    #neighbor.draw(self.win)

            self.draw()

            if current != self.start and current != self.end:
                current.make_closed()
                current.draw(self.win)

        return False

    def DFS(self):
        came_from = {}  # dict
        self.DFS_algorithm_rec(self.draw, self.grid, self.start, self.end, came_from)
        self.start.make_start()
        self.draw()

    def DFS_rec(self, draw, grid, start, end, came_from):  # draw supposed to be a function
        current = start
        current.make_closed()
        self.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if current == end:
            # make path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            self.ended = True
            return True

        for neighbor in current.neighbors:
            if (self.ended):
                return
            if not neighbor.is_closed():
                came_from[neighbor] = current
                self.DFS_algorithm_rec(draw, grid, neighbor, end, came_from)

        return

    def Dijkstra(self):
        count = 0
        current = self.start
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}  # dict
        distance = {spot: float("inf") for row in self.grid for spot in row}
        distance[self.start] = 0


        open_set_hash = {self.start}  # help to check if spot is in the open set

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]  # get the spot, the first current is the start node
            open_set_hash.remove(current)

            if current == self.end:
                # make path
                reconstruct_path(came_from, current, self.draw)
                self.end.make_end()
                self.start.make_start()
                return True

            for neighbor in current.neighbors:
                temp_d = distance[current] + 1

                if temp_d < distance[neighbor]:
                    came_from[neighbor] = current
                    distance[neighbor] = temp_d
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((distance[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            self.draw()

            if current != self.start:
                current.make_closed()

        return False

    def execute_callback(self, algorithm):
        getattr(self, algorithm)()


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



